# dealersearch2.py
from bs4 import BeautifulSoup
from app.dependencies.drivermanager import get_driver_manager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
from urllib.parse import quote
import os

class DealerSearch:
    def __init__(self, make, postcode, radius):
        self.make = make
        self.postcode = postcode
        self.radius = radius
        self.driver_manager = get_driver_manager()
        self.driver = None
        self.base_url = "https://www.autotrader.co.uk/cars/dealers/search"
        self.csv_file_path = 'output/extracted_dealership_info.csv'

    def setup_driver(self):
        """Initialize the WebDriver."""
        self.driver = self.driver_manager.get_driver()

    def generate_url(self):
        """Generate the URL for the dealership search based on input parameters."""
        encoded_postcode = quote(self.postcode)
        return f"{self.base_url}?advertising-locations=at_cars&forSale=on&make={self.make}&model=&postcode={encoded_postcode}&radius={self.radius}&sort=distance&toOrder=on"

    def accept_cookies(self):
        """Click the 'Accept All' button to handle cookie consent."""
        try:
            accept_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="notice"]/div[4]/button[3]'))
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(accept_button).perform()
            time.sleep(1)
            accept_button.click()
            time.sleep(1)
        except Exception as e:
            print(f"No accept button found: {e}")

    def extract_dealership_info(self, writer, url):
        """Extract information from the dealership page and write to CSV."""
        self.driver.get(url)
        time.sleep(2)  # Wait for the page to load
        self.accept_cookies()

        while True:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            listings = soup.find_all('a', {'data-testid': 'search-listing-title'})

            if not listings:
                print("No listings found on the page.")
                break

            for listing in listings:
                extracted_html = str(listing)
                writer.writerow([url, extracted_html])

            try:
                next_button = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="pagination-next"]'))
                )
                actions = ActionChains(self.driver)
                actions.move_to_element(next_button).perform()
                time.sleep(3)
                repo_path = "/app/"  # Adjust for Docker
                screenshot_path = os.path.join(repo_path, "screenshot.png")
        
                self.driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved at {screenshot_path}.")
                time.sleep(2)
        
                print("Page title is:", self.driver.title)
                next_button.click()
                time.sleep(3)
            except Exception as e:
                print(f"Only one page found or unable to click 'Next': {e}")
                break

    def run(self):
        """Main method to run the dealership search process."""
        self.setup_driver()
        url = self.generate_url()

        try:
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['URL', 'Extracted HTML'])  # Write the header

                self.extract_dealership_info(writer, url)
            print(f"Data successfully written to {self.csv_file_path}")
        except Exception as e:
            print(f"Error writing to CSV file: {e}")
        finally:
            if self.driver:
                self.driver.quit()

def search_dealerships(make, postcode, radius):
    """Function to instantiate the DealerSearch class and start the search process."""
    dealer_search = DealerSearch(make, postcode, radius)
    dealer_search.run()

if __name__ == '__main__':
    search_dealerships("Audi", "SW6 1DQ", 1)
