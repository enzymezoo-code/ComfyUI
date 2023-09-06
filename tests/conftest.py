import os
import pytest

# Command line arguments for pytest
def pytest_addoption(parser):
    parser.addoption('--output_dir', action="store", default='tests/inference/samples/test', help='Output directory for generated images')
    parser.addoption("--listen", type=str, default="127.0.0.1", metavar="IP", nargs="?", const="0.0.0.0", help="Specify the IP address to listen on (default: 127.0.0.1). If --listen is provided without an argument, it defaults to 0.0.0.0. (listens on all)")
    parser.addoption("--port", type=int, default=8188, help="Set the listen port.")

# This initializes args at the beginning of the test session
@pytest.fixture(scope="session", autouse=True)
def args_pytest(pytestconfig):
    args = {}
    args['output_dir'] = pytestconfig.getoption('output_dir')
    args['listen'] = pytestconfig.getoption('listen')
    args['port'] = pytestconfig.getoption('port')

    os.makedirs(args['output_dir'], exist_ok=True)

    return args

def pytest_collection_modifyitems(items):
    # Modifies items so tests run in the correct order
    
    LAST_TESTS = ['test_quality']

    module_name_map = {item.module.__name__: item for item in items}

    # Move the last tests to the end
    for test in LAST_TESTS:
        if test in module_name_map:
            items.append(module_name_map[test])
            items.remove(module_name_map[test])
