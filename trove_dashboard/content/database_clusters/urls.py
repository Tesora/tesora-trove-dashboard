# Copyright (c) 2014 eBay Software Foundation
# Copyright 2015 HP Software, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf.urls import include  # noqa
from django.conf.urls import url  # noqa

from trove_dashboard.content.database_clusters.configurations import (
    urls as configurations_urls)
from trove_dashboard.content.database_clusters.couchbase import (
    urls as couchbase_urls)
from trove_dashboard.content.database_clusters.database import (
    urls as database_urls)
from trove_dashboard.content.database_clusters.upgrade import (
    urls as upgrade_urls)
from trove_dashboard.content.database_clusters.user import (
    urls as user_urls)
from trove_dashboard.content.database_clusters import views

BASECLUSTERS = r'^(?P<cluster_id>[^/]+)/%s'
CLUSTERS = BASECLUSTERS + '$'
BASEINSTANCES = r'^(?P<instance_id>[^/]+)/%s'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^launch$', views.LaunchClusterView.as_view(), name='launch'),
    url(r'^(?P<cluster_id>[^/]+)/$', views.DetailView.as_view(),
        name='detail'),
    url(CLUSTERS % 'cluster_grow_details',
        views.ClusterGrowView.as_view(),
        name='cluster_grow_details'),
    url(CLUSTERS % 'add_instance',
        views.ClusterAddInstancesView.as_view(),
        name='add_instance'),
    url(CLUSTERS % 'cluster_shrink_details',
        views.ClusterShrinkView.as_view(),
        name='cluster_shrink_details'),
    url(CLUSTERS % 'reset_password',
        views.ResetPasswordView.as_view(),
        name='reset_password'),
    url(CLUSTERS % 'backup_instance',
        views.BackupInstanceView.as_view(),
        name='backup_instance'),
    url(BASEINSTANCES % 'couchbase/',
        include(couchbase_urls, namespace='couchbase')),
    url(BASECLUSTERS % 'configurations/',
        include(configurations_urls, namespace='configurations')),
    url(BASECLUSTERS % 'database/',
        include(database_urls, namespace='database')),
    url(BASECLUSTERS % 'upgrade/',
        include(upgrade_urls, namespace='upgrade')),
    url(BASECLUSTERS % 'user/',
        include(user_urls, namespace='user')),
]
