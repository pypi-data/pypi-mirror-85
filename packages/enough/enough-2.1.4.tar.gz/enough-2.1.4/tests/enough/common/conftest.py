def pytest_configure(config):
    config.addinivalue_line("markers", "openstack_integration: mark tests "
                            "which require OpenStack credentials")
