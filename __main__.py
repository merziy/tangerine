# Main entry for the program
import json
import os
import csv
from urllib.parse import urlsplit
from scrapy.crawler import CrawlerProcess
from sitecrawler.spiders.sitecrawler import SiteCrawler
from scrapy.utils.project import get_project_settings
from lighthouse import LighthouseRunner

def main():
    domain = input("Enter the domain to test (e.g., juicyorange.com): ")
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(SiteCrawler, domain=domain)
    process.start()

    with open('output.json') as f:
        url_list = json.load(f)
        urls = [url['url'] for url in url_list]
        os.remove('output.json')
        print('Removed json feed output.json file')

        additional_settings = [
            '--only-categories=accessibility'
        ]

        with open('urls.csv', 'w', newline='') as file:
            # Create a CSV writer object
            fieldnames = ['URL', 'Audit', 'Status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the base URL and Lighthouse Accessibility score above the fieldnames
            baseUrl = urlsplit(urls[0]).scheme + '://' + urlsplit(urls[0]).netloc
            runner = LighthouseRunner(baseUrl, 'desktop', quiet=False, additional_settings=additional_settings)
            score = runner.report.score['accessibility']

            # Write the rows with the base URL and the score
            writer.writerow({'URL': f'URL: {baseUrl} | Score: {score}'})
            writer.writeheader()

            for url in urls:
                runner = LighthouseRunner(url, 'desktop', quiet=False, additional_settings=additional_settings)

                accessibility_audits = runner.report.audits(0.86)['accessibility']
                passed_audits = accessibility_audits.passed
                failed_audits = accessibility_audits.failed

                for audit in passed_audits:
                    writer.writerow({'URL': url, 'Audit': audit.title, 'Status': 'Passed'})

                for audit in failed_audits:
                    writer.writerow({'URL': url, 'Audit': audit.title, 'Status': 'Failed'})

        print(f"Lighthouse reports written to the CSV file.")

if __name__ == "__main__":
    main()
