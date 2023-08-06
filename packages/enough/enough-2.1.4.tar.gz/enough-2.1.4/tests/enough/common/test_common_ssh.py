import pytest

from enough import settings
from enough.common.openstack import Stack
from enough.common.ssh import SSH


@pytest.mark.openstack_integration
def test_ssh(openstack_name):
    d = {
        'name': openstack_name,
        'flavor': 's1-2',
        'port': '22',
    }
    s = Stack(settings.CONFIG_DIR, d)
    s.set_public_key('infrastructure_key.pub')
    s.create_or_update()
    ssh = SSH(settings.CONFIG_DIR, domain='enough.community')
    r = ssh.ssh(openstack_name, ['uptime'], interactive=False)
    s.delete()
    assert r.returncode == 0
    assert 'load average' in r.stdout.decode('utf-8')
