from bs4 import BeautifulSoup
from app.dependencies.drivermanager import DriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import os

class Script3:
    def __init__(self):
        self.driver_manager = DriverManager()
        self.driver = None
        self.input_csv = 'output/working.csv'
        self.output_csv = 'output/maybe.csv'

    def setup_driver(self):
        """Initialize the WebDriver."""
        self.driver = self.driver_manager.get_driver()

    def read_dealer_ids(self):
        """Reads dealer IDs from the input CSV file."""
        dealer_ids = []
        with open(self.input_csv, 'r') as dealer_file:
            reader = csv.DictReader(dealer_file)
            for row in reader:
                dealer_ids.append(row['Identifier'])
        return dealer_ids

    def process_dealers(self):
        """Processes each dealer ID, navigates through the pages, and extracts data."""
        dealer_ids = self.read_dealer_ids()
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Extracted Li HTML'])  # Write the header row

            for dealer_id in dealer_ids:
                url = f"https://www.autotrader.co.uk/retailer/stock?advertising-location=at_cars&advertising-location=at_profile_cars&dealer={dealer_id}&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&advertising-location=at_cars&advertising-location=at_profile_cars&sort=price-desc"
                self.driver.get(url)
                time.sleep(4)  # Wait for the page to load
                self.scroll_and_extract(url, writer)

    def scroll_and_extract(self, url, writer):
        """Scrolls through the page, extracts data, and writes it to the CSV."""
        while True:
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                back_to_top_icon = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'i.icon-chevron'))
                )
                actions = ActionChains(self.driver)
                actions.move_to_element(back_to_top_icon).perform()
                time.sleep(2)  # Wait for the page to load more results

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break  # Stop scrolling if no new results are loaded
            except Exception as e:
                print(f"Error during scrolling: {e}")
                break

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        list_items = soup.find_all('li')

        for li in list_items:
            a_tag = li.find('a', href=True)
            if a_tag and 'car-details' in a_tag['href']:  # Ensure it is a car-details link
                li_html = str(li)
                writer.writerow([url, li_html])

    def run(self):
        """Runs the main script logic."""
        self.setup_driver()
        try:
            self.process_dealers()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        print(f"Data successfully written to {self.output_csv}")

# Example usage
if __name__ == '__main__':
    script3 = Script3()
    script3.run()
