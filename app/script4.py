import csv
from bs4 import BeautifulSoup
import re

class Script4:
    def __init__(self):
        self.input_csv = 'output/maybe.csv'  # Path to the CSV with raw HTML snippets
        self.working_csv = 'output/working.csv'  # Path to the CSV with dealership names and identifiers
        self.output_csv = 'output/yessir.csv'  # Path to the CSV where parsed data will be saved

    def load_dealership_data(self, file_path):
        """Loads dealership data from the working CSV file."""
        dealership_dict = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                dealership_dict[row['Identifier']] = row['Dealership Name']
        return dealership_dict

    def parse_car_data(self, html_snippet, dealer_name):
        """Parses car data from the HTML snippet."""
        soup = BeautifulSoup(html_snippet, 'html.parser')
        
        # Extract the title
        title = soup.find('h2').text if soup.find('h2') else ''
        
        # Extract the details
        details = soup.find('p').text if soup.find('p') else ''
        
        # Extract the condition
        condition = ''
        condition_tags = soup.find_all('p')
        for p in condition_tags:
            if 'MOT' in p.text or 'condition' in p.text.lower():
                condition = p.text
                break
        
        # Extract the price
        price = soup.find('h2', class_='vehicle-price').text if soup.find('h2', class_='vehicle-price') else ''
        
        # Extract the price indicator
        price_indicator = soup.find('div', class_='price-indicator-gauge__lozenge').text if soup.find('div', class_='price-indicator-gauge__lozenge') else ''
        
        # Extract the image URLs
        images = ' | '.join([img['src'] for img in soup.find_all('img', class_='list-image')])
        
        return [title, details, condition, dealer_name, price, price_indicator, images]

    def process_html_snippets(self):
        """Processes HTML snippets from the input CSV and writes parsed data to the output CSV."""
        dealership_dict = self.load_dealership_data(self.working_csv)
        
        with open(self.input_csv, 'r', encoding='utf-8') as infile, open(self.output_csv, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            writer.writerow(['Title', 'Details', 'Condition', 'Dealer Location', 'Price', 'Price Indicator', 'Images'])  # Write the header

            next(reader)  # Skip the header of the input file
            for row in reader:
                url, html_snippet = row
                identifier_match = re.search(r'dealer=(\d+)', url)
                if identifier_match:
                    identifier = identifier_match.group(1)
                    dealer_name = dealership_dict.get(identifier, 'Unknown Dealer')
                else:
                    dealer_name = 'Unknown Dealer'
                
                parsed_data = self.parse_car_data(html_snippet, dealer_name)
                writer.writerow(parsed_data)

    def run(self):
        """Runs the script to process HTML snippets and save parsed data."""
        self.process_html_snippets()
        print(f'Parsed data has been written to {self.output_csv}')

# Example usage
if __name__ == '__main__':
    script4 = Script4()
    script4.run()
