import pytest
import json
from dataclasses import dataclass
from tools.ui.base.browser import Browser
from tools.ui.screens.home_page import HomePage

def pytest_addoption(parser):
    """
    Define command-line options for pytest.
    """
    parser.addoption(
        "--environment", 
        action="store", 
        default="staging",  # Default value for environment
        help="Specify the test environment (e.g., staging, production)"
    )
    parser.addoption(
        "--device_name", 
        action="store", 
        default=None,  # No default, will use config if not provided
        help="Specify the mobile device name (e.g., iPhone X, Galaxy S5), use config if Not"
    )
    parser.addoption(
        "--is_local", 
        action="store_true",  
        default=True,  
        help="Boolean flag to specify if tests should run on local machine (True by default)"
    )

@dataclass
class UI:
    home_page: HomePage = None
    device_name: str = None
    environment: str = None
    url: str = None
    driver: object = None

def load_devices_from_json():
    """
    Function to load devices from the JSON config file.
    """
    with open('config/devices_config.json') as json_file:
        devices = json.load(json_file)
    return devices

def load_environment_config(environment):
    """
    Load the environment-specific configurations from a JSON file.
    """
    with open('config/environment_config.json') as json_file:
        env_config = json.load(json_file)
    return env_config.get(environment, {})

def get_devices_list(metafunc):
    """
    Function to determine which devices to use.
    """
    device_name = metafunc.getoption("--device_name")
    if device_name:
        return [device_name]
    else:
        devices = load_devices_from_json()
        return [device['device_name'] for device in devices]

@pytest.fixture
def args(request):
    """
    Fixture to provide parsed command-line arguments and environment config.
    """
    environment = request.config.getoption("--environment")
    env_config = load_environment_config(environment)
    
    return {
        'environment': environment,
        'device_name': request.config.getoption("--device_name"),
        'is_local': request.config.getoption("--is_local"),
        'url': env_config.get("url", "")
    }

def pytest_generate_tests(metafunc):
    """
    Pytest hook to generate dynamic parameters for the device_name fixture.
    """
    if "device_name" in metafunc.fixturenames:
        devices = get_devices_list(metafunc.config)
        metafunc.parametrize("device_name", devices)

@pytest.fixture
def device_name(request):
    """
    Fixture to return the dynamically generated device name.
    """
    return request.param  # Use the param passed by pytest_generate_tests

@pytest.fixture
def driver(device_name, request, args):
    """
    Fixture to initialize and return the browser driver.
    """
    browser = Browser()
    is_local = request.config.getoption("--is_local")

    driver_instance = browser.browser_driver(
        browser_name="chrome",              
        is_headless=not is_local,           
        device_name=device_name
    )
    driver_instance.get(args['url'])
    yield driver_instance
    driver_instance.quit()

@pytest.fixture
def ui(driver, args, device_name):
    """
    Fixture to initialize and return the UI context, including driver, home page, and any relevant data.
    """
    # Initialize the HomePage object
    home_page = HomePage(driver)

    # Return a UI object containing all required data
    return UI(
        home_page=home_page,
        device_name=device_name,
        environment=args['environment'],
        url=args['url'],
        driver=driver
    )