

def pytest_addoption(parser):
    parser.addoption("--conffile", action="append", default=[])


def pytest_generate_tests(metafunc):
    if 'conffile' in metafunc.fixturenames:
        metafunc.parametrize("conffile", metafunc.config.option.conffile)
