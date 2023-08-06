import json
import os
import pytest
import sh
import shutil
import yaml

from enough import settings
from enough.common import Enough
from enough.common.openstack import OpenStackBase, OpenStack


@pytest.mark.openstack_integration
def test_clone_and_destroy(tmpdir):
    test_clouds = 'inventory/group_vars/all/clouds.yml'

    clone_override_dir = f'{tmpdir}/clone-override'
    shutil.copytree('tests/enough/common/test_init/clone-override',
                    clone_override_dir)
    original_domain = 'original.com'
    original_config_dir = f'{tmpdir}/{original_domain}'
    shutil.copytree('tests/enough/common/test_init/backup',
                    original_config_dir)
    password = 'PASSWORD'
    open(f'{original_config_dir}.pass', 'w').write(password)
    shutil.copy('infrastructure_key', f'{original_config_dir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{original_config_dir}/infrastructure_key.pub')
    original_all_dir = f'{original_config_dir}/inventory/group_vars/all'
    os.makedirs(original_all_dir)
    original_clouds = f'{original_all_dir}/clouds.yml'
    shutil.copyfile(test_clouds, original_clouds)
    assert not os.path.exists(f'{original_all_dir}/internal_network.yml')

    original = Enough(original_config_dir, settings.SHARE_DIR,
                      domain=original_domain,
                      driver='openstack')
    assert original.openstack.o.server.list().strip() == ''

    clone_domain = 'clone.com'
    clone = original.clone(clone_domain, 'clone', True)

    assert password == open(f'{clone.config_dir}.pass').read()
    assert 'REPLACED CONTENT' == open(
        f'{clone.config_dir}/inventory/host_vars/to-replace.yml').read().strip()
    assert clone.openstack.o.server.list().strip() == ''
    clone_all_dir = f'{clone.config_dir}/inventory/group_vars/all'
    assert os.path.exists(f'{clone_all_dir}/internal_network.yml')

    assert os.path.exists(clone.config_dir)
    clone.destroy()
    assert not os.path.exists(clone.config_dir)


def create_enough(tmpdir, dotenough, **kwargs):
    clouds = 'inventory/group_vars/all/clouds.yml'

    enough_domain = 'enough.com'
    enough_config_dir = f'{tmpdir}/{enough_domain}'
    shutil.copytree(f'tests/enough/common/test_init/{dotenough}',
                    enough_config_dir)
    shutil.copy('infrastructure_key', f'{enough_config_dir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{enough_config_dir}/infrastructure_key.pub')
    enough_all_dir = f'{enough_config_dir}/inventory/group_vars/all'
    os.makedirs(enough_all_dir)
    enough_clouds = f'{enough_all_dir}/clouds.yml'
    shutil.copyfile(clouds, enough_clouds)

    enough = Enough(enough_config_dir, settings.SHARE_DIR,
                    domain=enough_domain,
                    driver='openstack',
                    **kwargs)
    return enough


def test_clone_clobber(tmpdir):
    original = create_enough(tmpdir, 'copy')
    clone_domain = 'clone.com'
    clone = original.clone(clone_domain, 'clone', False)
    assert os.path.exists(f'{clone.config_dir}')
    stone = f'{clone.config_dir}/STONE'
    open(stone, 'w').write('INSIDE')

    assert os.path.exists(stone)
    clone = original.clone(clone_domain, 'clone', False)
    assert os.path.exists(stone)
    clone = original.clone(clone_domain, 'clone', True)
    assert not os.path.exists(stone)


def create_and_clone_server_and_volume(tmpdir):
    original = create_enough(tmpdir, 'backup')
    original.set_args(name='sample', playbook='enough-playbook.yml')
    original.service.create_or_update()

    clone_domain = 'clone.com'
    clone = original.clone(clone_domain, 'clone', True)
    clone.set_args(name='sample', playbook='enough-playbook.yml')
    clone.service.create_or_update()

    return (original, clone)


@pytest.mark.openstack_integration
def test_clone_create_service(tmpdir):
    try:
        (original, clone) = create_and_clone_server_and_volume(tmpdir)
        assert 'sample-host' in original.openstack.o.server.list()
        assert 'sample-volume' in original.openstack.o.volume.list()
        assert 'sample-host' in clone.openstack.o.server.list()
        assert 'sample-volume' in clone.openstack.o.volume.list()
    finally:
        for cloud in ('production', 'clone'):
            o = OpenStack(settings.CONFIG_DIR, cloud=cloud)
            # comment out the following line to re-use the content of the regions and save time
            o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_create_copy_host(tmpdir):
    try:
        enough = create_enough(tmpdir, 'copy')
        if 'copy-volume' not in enough.openstack.o.volume.list():
            enough.openstack.o.volume.create('--size', '1', 'copy-volume')
        ip = enough.create_copy_host('copy-from-host', 'some-volume', 'copy-volume')
        r = sh.ssh('-oStrictHostKeyChecking=no',
                   '-i', enough.dotenough.private_key(), f'root@{ip}', 'id')
        assert 'uid=0(root)' in r
        r = sh.ssh('-oStrictHostKeyChecking=no',
                   '-i', enough.dotenough.private_key(), f'root@{ip}', 'mountpoint', '/srv').strip()
        assert r == '/srv is a mountpoint'
    finally:
        o = OpenStack(settings.CONFIG_DIR)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_create_volume_from_snapshot(tmpdir):
    try:
        e = create_enough(tmpdir, 'backup')
        e.set_args(name='sample', playbook='enough-playbook.yml')
        e.service.create_or_update()
        e.openstack.backup_create(['sample-volume'])
        snapshot = f'{e.openstack.backup_date()}-sample-volume'
        assert snapshot in e.openstack.o.volume.snapshot.list()

        volume = 'test-volume'
        e.create_volume_from_snapshot(snapshot, volume)

        assert volume in e.openstack.o.volume.list()

    finally:
        o = OpenStack(settings.CONFIG_DIR)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_clone_volume_from_snapshot(tmpdir):
    try:
        original = create_enough(tmpdir, 'backup')
        original.set_args(name='sample', playbook='enough-playbook.yml')
        original.service.create_or_update()
        ip = original.hosts.load().get_ip('sample-host')
        sh.ssh('-oStrictHostKeyChecking=no',
               '-i', original.dotenough.private_key(), f'debian@{ip}', 'touch', '/srv/STONE')
        sh.ssh('-oStrictHostKeyChecking=no',
               '-i', original.dotenough.private_key(), f'debian@{ip}', 'sync')
        original.openstack.backup_create(['sample-volume'])
        snapshot = f'{original.openstack.backup_date()}-sample-volume'
        assert snapshot in original.openstack.o.volume.snapshot.list()

        clone_domain = 'clone.com'
        clone = original.clone(clone_domain, 'clone', True)

        (from_ip, to_ip, from_volume, to_volume) = original._clone_volume_from_snapshot_body(
            clone, snapshot)

        assert sh.ssh('-oStrictHostKeyChecking=no',
                      '-i', original.dotenough.private_key(), f'root@{from_ip}',
                      'test', '-e', '/srv/STONE').exit_code == 0
        assert sh.ssh('-oStrictHostKeyChecking=no',
                      '-i', clone.dotenough.private_key(), f'root@{to_ip}',
                      'test', '!', '-e', '/srv/STONE').exit_code == 0
        original._rsync_copy_host(from_ip, to_ip)
        assert sh.ssh('-oStrictHostKeyChecking=no',
                      '-i', clone.dotenough.private_key(), f'root@{to_ip}',
                      'test', '-e', '/srv/STONE').exit_code == 0

        original._clone_volume_from_snapshot_cleanup(clone, from_volume)

    finally:
        for cloud in ('production', 'clone'):
            o = OpenStack(settings.CONFIG_DIR, cloud=cloud)
            # comment out the following line to re-use the content of the regions and save time
            o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_create_service_matching_snapshot(tmpdir):
    try:
        enough = create_enough(tmpdir, 'backup')
        host = enough.create_service_matching_snapshot('2020-02-20-sample-volume')
        assert host == 'sample-host'
        assert 'sample-volume' in enough.openstack.o.volume.list()

    finally:
        o = OpenStack(settings.CONFIG_DIR)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_restore_remote(tmpdir):
    try:
        original = create_enough(tmpdir, 'backup')
        original.set_args(name='sample', playbook='enough-playbook.yml')
        original.service.create_or_update()
        ip = original.hosts.load().get_ip('sample-host')

        sh.ssh('-oStrictHostKeyChecking=no',
               '-i', original.dotenough.private_key(), f'debian@{ip}', 'touch', '/srv/STONE')
        original.openstack.backup_create(['sample-volume'])
        snapshot = f'{original.openstack.backup_date()}-sample-volume'
        assert snapshot in original.openstack.o.volume.snapshot.list()

        clone = original.restore_remote('test.com', 'clone', True, snapshot)
        assert 'sample-volume' in clone.openstack.o.volume.list()
        hosts = clone.hosts.load()
        OpenStackBase.wait_for_ssh(hosts.get_ip('sample-host'), hosts.get_port('sample-host'))
        assert sh.ssh('-oStrictHostKeyChecking=no',
                      '-i', clone.dotenough.private_key(), f'debian@{ip}',
                      'test', '-e', '/srv/STONE').exit_code == 0

    finally:
        for cloud in ('production', 'clone'):
            o = OpenStack(settings.CONFIG_DIR, cloud=cloud)
            # comment out the following line to re-use the content of the regions and save time
            o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_restore_local(tmpdir):
    try:
        e = create_enough(tmpdir, 'backup')
        e.set_args(name='sample', playbook='enough-playbook.yml')
        e.service.create_or_update()
        ip = e.hosts.load().get_ip('sample-host')

        sh.ssh('-oStrictHostKeyChecking=no',
               '-i', e.dotenough.private_key(), f'debian@{ip}', 'touch', '/srv/STONE')
        e.openstack.backup_create(['sample-volume'])
        sh.ssh('-oStrictHostKeyChecking=no',
               '-i', e.dotenough.private_key(), f'debian@{ip}', 'rm', '/srv/STONE')
        snapshot = f'{e.openstack.backup_date()}-sample-volume'
        assert snapshot in e.openstack.o.volume.snapshot.list()

        assert e == e.restore_local(snapshot)
        assert 'sample-volume' in e.openstack.o.volume.list()
        OpenStackBase.wait_for_ssh(e.hosts.get_ip('sample-host'), e.hosts.get_port('sample-host'))
        assert sh.ssh('-oStrictHostKeyChecking=no',
                      '-i', e.dotenough.private_key(), f'debian@{ip}',
                      'test', '-e', '/srv/STONE').exit_code == 0

    finally:
        o = OpenStack(settings.CONFIG_DIR)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.openstack_integration
def test_create_missings(tmpdir):
    try:
        enough = create_enough(tmpdir, 'create-missings')
        r = enough.create_missings(['bind-host'])
        assert 'bind-host' in r
        internal_dns = enough.openstack.o.subnet.show(
            '--format=json', '-c', 'dns_nameservers', 'internal')
        internal_dns = json.loads(internal_dns.stdout)
        assert len(internal_dns['dns_nameservers']) == 1
        bind_internal_ip = enough.openstack.server_ip_in_network('bind-host', 'internal')
        assert bind_internal_ip == internal_dns['dns_nameservers'][0]
    finally:
        o = OpenStack(settings.CONFIG_DIR)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


def test_replace_production(tmpdir):
    target_cloud = 'clone'
    clouds = {
        'clouds': {
            target_cloud: 'CLONE',
            'production': 'PRODUCTION',
        }
    }
    clouds_path = f'{tmpdir}/clouds.yml'
    open(clouds_path, 'w').write(yaml.dump(clouds))
    Enough.replace_production(clouds_path, target_cloud)
    clouds = yaml.load(open(clouds_path))
    assert clouds['clouds']['production'] == 'CLONE'
    assert target_cloud not in clouds['clouds']


def test_volume_from_snapshot():
    volume = 'NAME'
    snapshot = f'2010-07-08-{volume}'
    assert Enough.volume_from_snapshot(snapshot) == volume


def test_host_from_snapshot(tmpdir):
    e = create_enough(tmpdir, 'backup')
    host = 'sample-host'
    snapshot = f'2010-07-08-sample-volume'
    assert e.host_from_snapshot(snapshot) == host


@pytest.mark.openstack_integration
def test_volume_resize(tmpdir):
    try:
        enough = create_enough(tmpdir, 'resize')
        enough.set_args(name='sample', playbook='enough-playbook.yml')
        enough.service.create_or_update()
        # False because the size does not change
        assert enough.volume_resize('sample-host', 'sample-volume') is False
        with pytest.raises(Enough.VolumeResizeUndefined):
            enough.volume_resize('other-host', 'other-volume')
        with pytest.raises(Enough.VolumeResizeNoSize):
            enough.volume_resize('nosize-host', 'nosize-volume')
    finally:
        o = OpenStack(settings.CONFIG_DIR)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


#
# Host
#
@pytest.mark.openstack_integration
def test_host_create_or_update(tmpdir, openstack_name):
    try:
        enough = create_enough(tmpdir, 'host')
        enough.set_args(name='new-host')
        info = enough.host.create_or_update()
        assert 'ipv4' in info
    finally:
        o = OpenStack(settings.CONFIG_DIR)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)
