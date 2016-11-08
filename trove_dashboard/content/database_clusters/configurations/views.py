# Copyright 2016 Tesora Inc.
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

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms as horizon_forms
from horizon.utils import memoized

from trove_dashboard import api
from trove_dashboard.content.database_clusters.configurations import forms


class AttachConfigurationView(horizon_forms.ModalFormView):
    form_class = forms.AttachConfigurationForm
    form_id = "attach_config_form"
    modal_header = _("Attach Configuration Group")
    modal_id = "attach_config_modal"
    template_name = ("project/databases/attach_config.html")
    submit_label = "Attach Configuration"
    submit_url = ('horizon:project:database_clusters:'
                  'configurations:attach_config')
    success_url = reverse_lazy('horizon:project:database_clusters:index')

    def get_context_data(self, **kwargs):
        context = (super(AttachConfigurationView, self)
                   .get_context_data(**kwargs))
        context['cluster_id'] = self.get_id()
        args = (self.get_id(),)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_initial(self):
        cluster_id = self.get_id()
        cluster = self.get_cluster()
        return {'cluster_id': cluster_id,
                'datastore': cluster.datastore.get('type', ''),
                'datastore_version': cluster.datastore.get('version', '')}

    @memoized.memoized_method
    def get_cluster(self):
        cluster_id = self.get_id()
        try:
            return api.trove.cluster_get(self.request, cluster_id)
        except Exception:
            msg = _('Unable to retrieve cluster details.')
            redirect = reverse('horizon:project:database_clusters:index',
                               args=[cluster_id])
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_id(self):
        return self.kwargs['cluster_id']
