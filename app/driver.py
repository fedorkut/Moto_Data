from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

class DriverManager:
    def __init__(self):
        self.driver = None
        self.selenium_hub_url = 'http://localhost:4444/wd/hub'  # Update to the Selenium Hub URL if different

    def setup_driver(self):
        """Initializes the WebDriver with specific options for Brave in a Selenium Grid."""
        options = webdriver.ChromeOptions()
        
        # Set options for Brave
        options.binary_location = '/usr/bin/brave-browser'  # Adjust this path if Brave is located elsewhere
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--disable-gpu")  # Recommended for headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-webrtc")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--headless=new")  # Ensure it's headless for running in containers
        
        # Desired capabilities for Brave
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['browserName'] = 'chrome'  # This should be 'chrome' since Brave is Chromium-based
        capabilities['goog:chromeOptions'] = options.to_capabilities()['goog:chromeOptions']

        # Connect to the Selenium Hub using Remote WebDriver
        self.driver = webdriver.Remote(
            command_executor=self.selenium_hub_url,
            desired_capabilities=capabilities
        )
        time.sleep(3)

    def get_driver(self):
        """Returns the initialized WebDriver instance."""
        if self.driver is None:
            self.setup_driver()
        return self.driver

    def quit_driver(self):
        """Quits the WebDriver session."""
        if self.driver:
            self.driver.quit()
            self.driver = None
