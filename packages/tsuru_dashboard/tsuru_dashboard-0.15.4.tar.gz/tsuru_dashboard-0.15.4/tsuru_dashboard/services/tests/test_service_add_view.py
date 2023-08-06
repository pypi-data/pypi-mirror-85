from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.services.views import ServiceAdd

import mock


class ServiceAddViewTest(TestCase):
    @mock.patch("requests.post")
    @mock.patch("requests.get")
    def test_post(self, get, post):
        get.return_value = mock.Mock(status_code=200)
        post.return_value = mock.Mock(status_code=201)
        data = {"name": "name", "team": "team", "description": "desc", "plan": "plan"}
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}
        response = ServiceAdd.as_view()(request, service_name="service")
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('service-list'), response.items()[2][1])
        post.assert_called_with(
            '{0}/services/service/instances'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'},
            data={"name": "name", "owner": "team", "description": "desc", "plan": "plan"})

    @mock.patch("requests.post")
    @mock.patch("requests.get")
    def test_post_with_tags(self, get, post):
        get.return_value = mock.Mock(status_code=200)
        post.return_value = mock.Mock(status_code=201)
        data = {
            "name": "name",
            "team": "myteam",
            "description": "mydescription",
            "plan": "myplan",
            "tags": " tag 1 , tag 2, tag 3  ,, , "
        }
        request = RequestFactory().post("/", data)
        request.session = {"tsuru_token": "admin"}
        response = ServiceAdd.as_view()(request, service_name="service")
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('service-list'), response.items()[2][1])
        post.assert_called_with(
            '{0}/services/service/instances'.format(settings.TSURU_HOST),
            headers={'authorization': 'admin'},
            data={
                "name": "name",
                "owner": "myteam",
                "description": "mydescription",
                "plan": "myplan",
                "tag": ["tag 1", "tag 2", "tag 3"]
            })

    @mock.patch("requests.get")
    def test_get(self, get):
        get.return_value = mock.Mock(status_code=200)
        request = RequestFactory().get("/")
        request.session = {"tsuru_token": "admin"}
        response = ServiceAdd.as_view()(request, service_name="service")
        self.assertEqual(200, response.status_code)
