from icinga2api.exceptions import Icinga2ApiException
from tests.icinga_helper import IcingaHelper
import pytest

testinfra_hosts = ['ansible://icinga-host']


class TestChecks(IcingaHelper):

    def test_icinga_host(self):
        objects = self.get_client().objects
        r = objects.get('Host', 'bind-host')
        assert r['attrs']['name'] == 'bind-host'
        with pytest.raises(Icinga2ApiException):
            objects.get('Host', 'deleted-host')

    def test_icinga_service(self, host):
        #  r = self.get_client().objects.list('Service', joins=['host.name'])
        with host.sudo():
            host.run("systemctl restart icinga2")
        assert self.is_service_ok('bind-host!ping4')
        domain = host.run("hostname -d").stdout.strip()
        assert self.is_service_ok('bind-host!Zone test.' + domain)
        assert self.is_service_ok('bind-host!Zone ' + domain)
