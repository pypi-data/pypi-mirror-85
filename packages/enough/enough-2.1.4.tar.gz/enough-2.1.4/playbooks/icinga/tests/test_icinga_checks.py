import re

from icinga2api.exceptions import Icinga2ApiException
from tests.icinga_helper import IcingaHelper
import pytest
import testinfra
import yaml

testinfra_hosts = ['ansible://icinga-host']


class TestChecks(IcingaHelper):

    def test_icinga_host(self):
        objects = self.get_client().objects
        r = objects.get('Host', 'bind-host')
        assert r['attrs']['name'] == 'bind-host'
        with pytest.raises(Icinga2ApiException):
            objects.get('Host', 'deleted-host')

    def test_icinga_version(self, pytestconfig):
        client = self.get_client()
        ret = client.status.list('IcingaApplication')
        version = ret['results'][0]['status']['icingaapplication']['app']['version']

        host = testinfra.get_host(f'ansible://{TestChecks.icinga_host}',
                                  ssh_identity_file=self.ssh_identity_file,
                                  ansible_inventory=self.inventory)
        host_vars = host.ansible.get_variables()
        expected_version = host_vars.get('icinga_version')
        if not expected_version:
            icinga2_common_defaults = 'playbooks/icinga/roles/icinga2_common/defaults/main.yml'
            expected_version = yaml.load(open(icinga2_common_defaults))['icinga_version']

        expected_version = expected_version.rsplit('.', 1)[0]
        assert re.search(expected_version, version)

    def test_disk(self):
        assert self.is_service_ok('website-host!disk')
        assert self.is_service_ok('packages-host!disk')

    def test_icinga_ntp_time(self):
        assert self.is_service_ok('website-host!systemd-timesyncd is working')

    def test_memory(self):
        assert self.is_service_ok('icinga-host!memory')
        assert self.is_service_ok('website-host!memory')
