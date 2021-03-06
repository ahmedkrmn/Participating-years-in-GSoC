import re
import requests
import csv
from bs4 import BeautifulSoup

sources = []  # [GSoC year, HTML Source]
# {Organization: [No of participations, [Participating Years]}
organizations = {}

with open('GSoC_archives.csv', 'r') as csv_read_file:
    csv_reader = csv.reader(csv_read_file)
    next(csv_reader)  # Skip the header
    for row in csv_reader:
        sources.append([row[0], requests.get(row[1]).text])

for source in sources:
    soup = BeautifulSoup(source[1], 'html.parser')
    # GSoC 2016 and later is scraped from the new archive website while older editions are from Google Melange Archive.
    class_str = 'organization-card__name' if int(
        source[0]) > 2015 else 'mdl-list__item-primary-content'
    names = soup.find_all(class_=class_str)
    for name in names:
        if class_str == 'organization-card__name':
            # All Extended ASCII characters are replaced with spaces to avoid inconsistencies
            name = re.sub('[^0-9a-zA-Z]+', ' ', name.text)
        else:
            name = re.sub('[^0-9a-zA-Z]+', ' ', name.a.text)
        organizations[name] = organizations.get(name, [0, []])
        organizations[name][0] += 1
        organizations[name][1].append(source[0])


with open('organization_years.csv', 'w', newline='') as csv_write_file:
    csv_writer = csv.writer(csv_write_file)
    csv_writer.writerow(['Organization', 'Years in GSoC', 'Total'])
    for key, value in sorted(organizations.items(), key=lambda x: (-x[1][0], x[0])):
        csv_writer.writerow([key, (', ').join(value[1]), value[0]])
