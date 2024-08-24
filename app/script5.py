import csv

class Script5:
    def __init__(self):
        self.input_csv = 'output/yessir.csv'
        self.output_csv = 'output/1000_checked.csv'

    def remove_duplicates(self):
        """Removes duplicate rows from the input CSV and writes unique rows to the output CSV."""
        unique_lines = set()

        with open(self.input_csv, 'r', encoding='utf-8') as infile, open(self.output_csv, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)
            header = next(reader)  # Read the header
            writer.writerow(header)  # Write the header to the output file

            for row in reader:
                row_tuple = tuple(row)
                if row_tuple not in unique_lines:
                    unique_lines.add(row_tuple)  # Add the row to the set
                    writer.writerow(row)  # Write the unique row to the output file

    def run(self):
        """Runs the script to remove duplicate rows from the CSV file."""
        self.remove_duplicates()
        print(f'Unique data has been written to {self.output_csv}')

# Example usage
if __name__ == '__main__':
    script5 = Script5()
    script5.run()
