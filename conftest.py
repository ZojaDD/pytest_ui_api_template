import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--testing-type",
        action="store",
        default="all",
        help="Type of tests to run: api, ui, or all"
    )

def pytest_collection_modifyitems(config, items):
    testing_type = config.getoption("--testing-type")

    if testing_type == "api":
        skip_ui = pytest.mark.skip(reason="Skipping UI tests")
        for item in items:
            if "ui" in item.nodeid:
                item.add_marker(skip_ui)
    elif testing_type == "ui":
        skip_api = pytest.mark.skip(reason="Skipping API tests")
        for item in items:
            if "api" in item.nodeid:
                item.add_marker(skip_api)