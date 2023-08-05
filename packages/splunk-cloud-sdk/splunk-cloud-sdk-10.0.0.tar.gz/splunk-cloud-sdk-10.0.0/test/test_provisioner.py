# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pytest

from splunk_sdk.base_client import BaseClient, HTTPError
from splunk_sdk.provisioner import Provisioner, CreateProvisionJobBody
from test.fixtures import get_test_client_provisioner as test_client  # NOQA


@pytest.mark.usefixtures("test_client")  # NOQA
def test_invalid_create_job(test_client: BaseClient):
    provisioner = Provisioner(test_client)
    with pytest.raises(HTTPError) as excinfo:
        provisioner.create_provision_job(CreateProvisionJobBody(tenant="splunk"))
    err = excinfo.value
    assert(err is not None)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_invalid_get_provision_job(test_client: BaseClient):
    provisioner = Provisioner(test_client)
    with pytest.raises(HTTPError) as excinfo:
        provisioner.get_provision_job(-1)

    err = excinfo.value
    assert(err.http_status_code == 404)
    assert(err.code == "NotFound")


@pytest.mark.usefixtures("test_client")  # NOQA
def test_list_provision_jobs(test_client: BaseClient):
    provisioner = Provisioner(test_client)
    jobs = provisioner.list_provision_jobs()
    assert(len(jobs) == 0)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_tenant(test_client: BaseClient):
    provisioner = Provisioner(test_client)
    tenant_name = "testprovisionersdks"
    tenant = provisioner.get_tenant(tenant_name)
    assert(tenant.name == tenant_name)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_list_tenants(test_client: BaseClient):
    provisioner = Provisioner(test_client)
    tenant_name = "testprovisionersdks"
    tenants = provisioner.list_tenants()
    [t] = [t for t in tenants if t.name == tenant_name]
    assert(t.name == tenant_name)
