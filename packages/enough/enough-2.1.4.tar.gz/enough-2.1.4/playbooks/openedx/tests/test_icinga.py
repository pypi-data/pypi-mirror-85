from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://bind-host']

IcingaHelper.icinga_host = 'bind-host'


class TestChecks(IcingaHelper):

    def test_host(self):
        r = self.get_client().objects.get('Host', 'openedx-host')
        assert r['attrs']['name'] == 'openedx-host'

    def test_service(self, host):
        assert self.is_service_ok('openedx-host!openedX')
