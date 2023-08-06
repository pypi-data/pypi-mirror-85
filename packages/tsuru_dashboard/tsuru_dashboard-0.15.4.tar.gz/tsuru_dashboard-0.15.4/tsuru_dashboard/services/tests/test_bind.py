from mock import patch, Mock

from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse

from tsuru_dashboard import settings
from tsuru_dashboard.services.views import Bind


class BindViewTest(TestCase):
    @patch("requests.put")
    @patch("requests.get")
    def test_view(self, get, put):
        get.return_value = Mock(status_code=200)
        app = "app"
        request = RequestFactory().post("/", {"app": app})
        request.session = {"tsuru_token": "admin"}
        instance = "service"
        service = "service"

        response = Bind.as_view()(request, service=service, instance=instance)

        self.assertEqual(302, response.status_code)
        url = reverse('service-detail', args=[service, instance])
        self.assertEqual(url, response.items()[2][1])
        url = '{}/services/{}/instances/{}/{}'.format(settings.TSURU_HOST, service, instance, app)
        put.assert_called_with(url, headers={'authorization': 'admin'})
