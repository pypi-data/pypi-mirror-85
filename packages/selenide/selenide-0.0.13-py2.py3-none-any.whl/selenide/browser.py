from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities


def browser(name="chrome", driver=None, grid_url=None, options=None):
    if name not in ("chrome", "firefox"):
        raise WebDriverException(f"Un support driver {name}")
    elif name == "firefox":
        if grid_url:
            return webdriver.Remote(
                command_executor=grid_url,
                desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
                options=options,
            )
        return webdriver.Firefox(executable_path=driver, options=options)
    elif name == "chrome":
        if grid_url:
            return webdriver.Remote(
                command_executor=grid_url,
                desired_capabilities=DesiredCapabilities.CHROME.copy(),
                options=options,
            )
        return webdriver.Chrome(executable_path=driver, options=options)
