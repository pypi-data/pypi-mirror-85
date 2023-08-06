import requests
import grequests
import urllib
import json

from django.views.generic import TemplateView
from django.http import HttpResponse, Http404, JsonResponse, StreamingHttpResponse, QueryDict
from django.core.urlresolvers import reverse
from django.contrib import messages

from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter

from tsuru_dashboard import settings
from tsuru_dashboard.auth.views import LoginRequiredView
from tsuru_dashboard.admin.models import Node


class PoolList(LoginRequiredView, TemplateView):
    template_name = "admin/pool_list.html"

    def nodes_by_pool(self):
        url = "{}/docker/node".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        pools = {}

        if response.status_code != 204:
            data = response.json()
            nodes = data.get("nodes", [])

            for node in nodes:
                pool = Node(node).pool()
                nodes_by_pool = pools.get(pool, [])
                data = {"address": node["Address"], "status": node["Status"]}
                nodes_by_pool.append(data)
                pools[pool] = nodes_by_pool

            for pool in pools:
                pools[pool] = json.dumps(pools[pool])
        return sorted(pools.items())

    def get_context_data(self, **kwargs):
        context = super(PoolList, self).get_context_data(**kwargs)
        context.update({"pools": self.nodes_by_pool()})
        return context


class NodeInfo(LoginRequiredView, TemplateView):
    template_name = "admin/node_info.html"


class NodeInfoJson(LoginRequiredView):
    def get_containers(self, node_address):
        url = "{}/docker/node/{}/containers".format(settings.TSURU_HOST, node_address)
        return requests.get(url, headers=self.authorization)

    def get_node(self, address):
        url = "{}/docker/node".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)

        if response.status_code == 204:
            return None

        data = response.json()
        nodes = data.get("nodes", [])

        for node in nodes:
            if node["Address"] == address:
                return node

        return None

    def get(self, *args, **kwargs):
        address = kwargs["address"]
        node_dict = None
        node = self.get_node(address)
        if node:
            containers_rsp = self.get_containers(address)
            node = Node(node, containers_rsp)
            node_dict = node.to_dict()
            for container in node_dict["units"]:
                if "AppName" in container:
                    container["DashboardURL"] = reverse(
                        'app-info', kwargs={'app_name': container["AppName"]})
        return JsonResponse({
            "node": {
                "info": node_dict,
                "nodeRemovalURL": reverse('node-remove', kwargs={'address': address})
            }
        })


class ListDeploy(LoginRequiredView, TemplateView):
    template_name = "deploys/list_deploys.html"

    def get_context_data(self, **kwargs):
        context = super(ListDeploy, self).get_context_data(**kwargs)

        page = int(self.request.GET.get('page', '1'))

        skip = (page * 20) - 20
        limit = page * 20

        url = '{}/deploys?skip={}&limit={}'.format(settings.TSURU_HOST, skip, limit)

        response = requests.get(url, headers=self.authorization)

        if response.status_code == 204:
            deploys = []
        else:
            deploys = response.json()

        context['deploys'] = deploys

        if len(deploys) >= 20:
            context['next'] = page + 1

        if page > 0:
            context['previous'] = page - 1

        return context


class DeployInfo(LoginRequiredView, TemplateView):
    template_name = "deploys/deploy_details.html"

    def get_context_data(self, **kwargs):
        deploy_id = kwargs["deploy"]

        url = "{}/deploys/{}".format(settings.TSURU_HOST, deploy_id)
        response = requests.get(url, headers=self.authorization)

        if response.status_code > 399:
            raise Http404("Deploy does not exist")

        context = {"deploy": response.json()}

        diff = context["deploy"].get("Diff")
        if diff and diff != u'The deployment must have at least two commits for the diff.':
            format = HtmlFormatter()
            diff = highlight(diff, DiffLexer(), format)
        else:
            diff = None

        context["deploy"]["Diff"] = diff
        return context


class ListHealing(LoginRequiredView, TemplateView):
    template_name = "admin/list_healing.html"

    def get_context_data(self, **kwargs):
        context = super(ListHealing, self).get_context_data(**kwargs)
        url = '{}/docker/healing'.format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)
        formatted_events = []
        if response.status_code == 200:
            events = response.json() or []
            formatted_events = []

            for event in events:
                event['FailingContainer']['ID'] = event['FailingContainer']['ID'][:12]
                event['CreatedContainer']['ID'] = event['CreatedContainer']['ID'][:12]
                event['App'] = event['FailingContainer']['AppName']
                formatted_events.append(event)

        context.update({"events": formatted_events})
        return context


class PoolInfo(LoginRequiredView, TemplateView):
    template_name = "admin/pool_info.html"

    def nodes_by_pool(self, pool):
        url = "{}/docker/node".format(settings.TSURU_HOST)
        response = requests.get(url, headers=self.authorization)

        if response.status_code == 204:
            return []

        data = response.json()
        node_list = data.get("nodes", [])
        nodes = map(lambda n: Node(n), node_list)
        nodes = filter(lambda n: n.pool() == pool, nodes)

        url = "{}/docker/node/{}/containers"

        rs = []
        for node in nodes:
            u = url.format(settings.TSURU_HOST, node.address())
            rs.append(grequests.get(u, headers=self.authorization))

        units = grequests.map(rs)
        nodes_with_units = []

        for i, node in enumerate(nodes):
            node.load_units(units[i])
            nodes_with_units.append(node.to_dict())

        return nodes_with_units

    def get_context_data(self, **kwargs):
        context = super(PoolInfo, self).get_context_data(**kwargs)
        context.update({"nodes": self.nodes_by_pool(kwargs["pool"])})
        return context


class PoolMetrics(LoginRequiredView, TemplateView):
    template_name = "admin/pool_metrics.html"

    def get_grafana_url(self):
        if not settings.GRAFANA_POOL_DASHBOARD:
            return

        datasource = settings.GRAFANA_DATASOURCE_FOR_POOL.get(
            self.kwargs['pool'],
            settings.GRAFANA_DEFAULT_DATASOURCE
        )

        args = {
            'var-datasource': datasource,
            'var-pool': self.kwargs['pool'],
            'theme': settings.GRAFANA_THEME,
            'kiosk': settings.GRAFANA_KIOSK,
        }

        return settings.GRAFANA_POOL_DASHBOARD + '?' + urllib.urlencode(args)

    def get_context_data(self, **kwargs):
        context = super(PoolMetrics, self).get_context_data(**kwargs)
        context["grafana_url"] = self.get_grafana_url()
        return context


class NodeRemove(LoginRequiredView):
    def delete(self, *args, **kwargs):
        address = self.kwargs['address']
        params = QueryDict(self.request.body)

        msg = u"The value for '{}' parameter should be 'true' or 'false'"

        destroy = params.get("destroy", "false")
        if destroy not in ["true", "false"]:
            return HttpResponse(msg.format("destroy"), status=400)

        rebalance = params.get("rebalance", "false")
        if rebalance not in ["true", "false"]:
            return HttpResponse(msg.format("rebalance"), status=400)

        no_rebalance = "false" if rebalance == "true" else "true"

        response = requests.delete(
            '{}/docker/node/{}?remove-iaas={}&no-rebalance={}'.format(
                settings.TSURU_HOST, address, destroy, no_rebalance
            ),
            headers=self.authorization
        )

        if response.status_code > 399:
            return HttpResponse(response.text, status=response.status_code)

        return HttpResponse('Node was successfully removed', status=200)


class TemplateListJson(LoginRequiredView):

    def get(self, *args, **kwargs):
        templates = self.client.templates.list()
        return JsonResponse(templates, safe=False)


class NodeAdd(LoginRequiredView):

    def post(self, *args, **kwargs):
        resp = self.client.nodes.create(**self.request.POST.dict())

        for line in resp.iter_lines():
            msg_err = json.loads(line).get('Error')
            if msg_err:
                messages.error(self.request, msg_err, fail_silently=True)
                return HttpResponse(msg_err, status=500)

        messages.success(self.request, u'Node was successfully created', fail_silently=True)
        return HttpResponse('Node was successfully created', status=200)


class PoolRebalance(LoginRequiredView):

    def post(self, *args, **kwargs):
        def sending_stream():
            gen = ("{}<br>".format(line["Message"]) for line in self.client.pools.rebalance(pool=kwargs["pool"]))
            return gen

        return StreamingHttpResponse(sending_stream())
