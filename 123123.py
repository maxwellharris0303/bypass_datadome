import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
from concurrent.futures._base import TimeoutError
from concurrent.futures import thread
from concurrent.futures._base import Future
from concurrent.futures import _base
from threading import Lock


class ThreadSafeList:
    def __init__(self):
        self._list = []
        self._lock = Lock()

    def append(self, item):
        with self._lock:
            self._list.append(item)

    def extend(self, items):
        with self._lock:
            self._list.extend(items)

    def __iter__(self):
        return iter(self._list)


# Assuming the API key is correctly set
API_KEY = 'MLFVXFE8WP92644YD97BW4AVB286D74CCX6MFA8IN72RHGHZNWGHP4WJLMLHZK672KKNNOV17WR65HTB'


def get_company_description(api_key, linkedin_url):
    """Fetch the company's description from LinkedIn using ScrapingBee."""
    print(f"Making a request to {linkedin_url}")
    api_endpoint = 'https://app.scrapingbee.com/api/v1/'
    params = {
        'api_key': api_key,
        'url': linkedin_url,
        'render_js': 'true',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

    try:
        with requests.Session() as session:
            response = session.get(api_endpoint, params=params, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            description_tag = soup.find('meta', {'name': 'description'})
            return description_tag.get('content', '') if description_tag else 'Description not found in the HTML response.'
        else:
            raise Exception(f'Request failed with status code {response.status_code}')
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error for {linkedin_url}: {e}")
        raise


def update_progress(progress):
    """Displays or updates a console progress bar."""
    bar_length = 60
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length * progress))
    text = "\rPercent: [{0}] {1}% {2}".format("#" * block + "-" * (bar_length - block), progress * 100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def process_task(api_key, row):
    try:
        result = get_company_description(api_key, row['Company Linkedin Url'])
        row['About Us Text'] = result
        return row, None
    except Exception as e:
        return row, e


def main():
    csv_file_path = '111.csv'  # Path to your CSV file

    # Read the original CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        rows = list(csv_reader)
        fieldnames = csv_reader.fieldnames + ['About Us Text'] if 'About Us Text' not in csv_reader.fieldnames else csv_reader.fieldnames

    connection_errors = ThreadSafeList()  # Initialize a thread-safe list for connection error tracking

    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = []

        # Submit all tasks at once
        for row in rows:
            if 'About Us Text' not in row or not row['About Us Text']:
                future = executor.submit(process_task, API_KEY, row)
                futures.append(future)

        processed_count = 0  # Counter for processed URLs

        for future in as_completed(futures):
            try:
                row, error = future.result()
                if error:
                    print(f"Error on row {rows.index(row)}: {error}")
                    connection_errors.append((rows.index(row), row['Company Linkedin Url']))
                update_progress((processed_count + 1) / len(rows))
                processed_count += 1
            except TimeoutError:
                print("A task took too long to complete.")
            except Exception as e:
                print(f"An error occurred: {e}")

        # Bulk save the changes
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(rows)

    # Save connection errors to a separate file
    if connection_errors:
        error_file_path = 'connection_errors.csv'
        with open(error_file_path, mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Row Index', 'LinkedIn URL'])
            csv_writer.writerows(connection_errors)

    print("\nAll data has been processed and saved.")


if __name__ == '__main__':
    main()