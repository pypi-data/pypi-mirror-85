from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.PoolList.as_view(), name='pool-list'),
    url(r'^pool/(?P<pool>[\w\\.-]+)/rebalance/$', views.PoolRebalance.as_view(), name='pool-rebalance'),
    url(r'^pool/(?P<pool>[\w\\.-]+)/$', views.PoolInfo.as_view(), name='pool-info'),
    url(r'^pool/(?P<pool>[\w\\.-]+)/metrics/$', views.PoolMetrics.as_view(), name='pool-metrics'),
    url(r'^node/(?P<address>.+)/remove/$', views.NodeRemove.as_view(), name='node-remove'),
    url(r'^node/add/$', views.NodeAdd.as_view(), name='node-add'),
    url(r'^deploys/$', views.ListDeploy.as_view(), name='list-deploys'),
    url(r'^deploys/(?P<deploy>[\s\w@\.-]+)/$', views.DeployInfo.as_view(), name='deploy-info'),
    url(r'^healing/$', views.ListHealing.as_view(), name='list-healing'),
    url(r'^templates.json$', views.TemplateListJson.as_view(), name='template-list-json'),
    url(r'^(?P<address>.+)/containers/$', views.NodeInfoJson.as_view(), name='node-info-json'),
    url(r'^(?P<address>.+)/$', views.NodeInfo.as_view(), name='node-info'),
]
