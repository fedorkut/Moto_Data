import csv
from bs4 import BeautifulSoup

class Script2:
    def __init__(self):
        self.input_csv = 'output/extracted_dealership_info.csv'
        self.output_csv = 'output/working.csv'

    def parse_html(self, raw_html):
        """Parses the HTML content to extract the dealership name and identifier."""
        soup = BeautifulSoup(raw_html, 'html.parser')
        dealership_name = soup.find('h3').text if soup.find('h3') else ''
        href = soup.find('a')['href'] if soup.find('a') else ''
        identifier = href.split('-')[-1].split('?')[0] if href else ''  # Extracts the identifier
        return dealership_name, identifier

    def process_csv(self):
        """Processes the input CSV file to extract dealership information and writes to output CSV."""
        with open(self.input_csv, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read the header

            with open(self.output_csv, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(['Dealership Name', 'Identifier'])  # Write the header row

                for row in reader:
                    url, raw_html = row
                    dealership_name, identifier = self.parse_html(raw_html)
                    writer.writerow([dealership_name, identifier])  # Write extracted info to the output CSV

        print(f'Parsed data has been written to {self.output_csv}')

    def run(self):
        """Runs the script to process the CSV files."""
        self.process_csv()

# Example usage
if __name__ == '__main__':
    script2 = Script2()
    script2.run()
