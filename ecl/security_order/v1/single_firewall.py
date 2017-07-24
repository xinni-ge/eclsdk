# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from ecl.security_order import security_order_service
from ecl import resource2
from ecl import exceptions
from ecl import utils


class SingleFirewall(resource2.Resource):
    resource_key = None
    resources_key = None
    base_path = '/API/SoEntryFGS'
    service = security_order_service.SecurityOrderService()

    # Capabilities
    allow_create = True
    allow_get = True
    allow_delete = True
    allow_list = True
    allow_update = True

    # Properties
    #: Tenant ID of the owner (UUID).
    tenant_id = resource2.Body('tenant_id')
    #: List of following objects.
    #: operatingmode: Set "FW" or "UTM" to this value.
    #: licensekind: Set "02" or "08" as FW/UTM plan.
    #: azgroup: Availability Zone.
    gt_host = resource2.Body('gt_host')
    #: A: Create Single Constitution Device.
    sokind = resource2.Body('sokind', alternate_id=True)
    #: Messages are displayed in Japanese or English depending on this value.
    #: ja: Japanese, en: English. Default value is "en".
    locale = resource2.Body('locale')
    #: This value indicates normal or abnormal. 1:normal, 2:abnormal.
    code = resource2.Body('code')
    #: This message is shown when error has occurred.
    message = resource2.Body('message')
    #: Identification ID of Service Order.
    soid = resource2.Body('soId')
    #: This value indicates normal or abnormal. 1:normal, 2:abnormal.
    status = resource2.Body('status')
    #: Number of devices.
    records = resource2.Body('records')
    #: Device list.
    rows = resource2.Body('rows')
    #: List of device objects.
    devices = resource2.Body('devices')


    def list(self, session, locale=None):
        tenant_id = session.get_project_id()
        uri = '/API/ScreenEventFGSDeviceGet?tenant_id=%s' % tenant_id
        if locale is not None:
            uri += '&locale=%s' % locale
        headers = {'Content-Type': 'application/json'}
        resp = session.get(uri, endpoint_filter=self.service, headers=headers)
        body = resp.json()
        devices = []
        for row in body['rows']:
            device = {
                'internal_use': row['cell'][0],
                'rows': row['cell'][1],
                'host_name': row['cell'][2],
                'menu': row['cell'][3],
                'plan': row['cell'][4],
                'redundancy': row['cell'][5],
                'availability_zone': row['cell'][6],
                'zone_name': row['cell'][7],
            }
            devices.append(device)
        body.update({'devices': devices})
        self._translate_list_response(resp, body, has_body=True)
        return self

    def _translate_list_response(self, response, body, has_body=True):
        if has_body:
            if self.resource_key and self.resource_key in body:
                body = body[self.resource_key]

            body = self._filter_component(body, self._body_mapping())
            self._body.attributes.update(body)
            self._body.clean()

        headers = self._filter_component(response.headers,
                                         self._header_mapping())
        self._header.attributes.update(headers)
        self._header.clean()
