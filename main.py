from time import sleep, time
from random import randint
from warnings import warn
from requests import get
from IPython.display import clear_output
from bs4 import BeautifulSoup as bs

import database
import functions

# Preparing loop monitoring
start_time = time()
requests = 0

# For every page in the interval 1-443
pages = [str(i) for i in range(1,3)]
for page in pages:

    # Make a get request
    response = get('https://www.trabalhabrasil.com.br/vagas-empregos-em-sete-lagoas-mg?pagina=' + page)

    # Pause the loop
    sleep(randint(15, 30))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
    clear_output(wait=True)

    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # Break the loop if the number of requests is greater than expected
    if requests > 2:
        warn('Number of requests was greater than expected.')
        break

    # Parse the content of the request with BeautifulSoup
    soup = bs(response.text, 'html.parser')

    # Select all the 60 jobs containers from a single page
    jobsContainers = soup.find_all('div', class_='jg__container')

    for container in jobsContainers:
        if container.find('div', class_='jg__job') is not None:

            # Scrape title
            # Selecting the HTML
            titles = soup.select('.job__name')
            listTitle = []
            for title in titles:
                # Add only the text to a list
                listTitle.append(title.get_text(strip=True))

            # Scrape quantity
            quantities = soup.select('.job__name')
            listQuantity = []
            for quantity in quantities:
                listQuantity.append(quantity.get_text(strip=True))

            # Scrape company
            companies = soup.select('.job__company')
            listCompany = []
            for company in companies:
                listCompany.append(company.get_text(strip=True))

            # Scrape city
            cities = soup.select('.job__detail')
            listCity = []
            for city in cities:
                listCity.append(city.get_text(strip=True))

            # Scrape state
            states = soup.select('.job__detail')
            listState = []
            for state in states:
                listState.append(state.get_text(strip=True))

        database.savedb(functions.quantity(listQuantity), functions.title(listTitle), functions.company(listCompany), functions.city(listCity), functions.state(listState))