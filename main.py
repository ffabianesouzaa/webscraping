import urllib.request
from time import sleep, time
from random import randint
from warnings import warn
from requests import get
from bs4 import BeautifulSoup as bs

import database
import functions

# Preparing loop monitoring
start_time = time()
requests = 0

# For every page
pages = [str(i) for i in range(1, 6)]
for page in pages:

    # Internet connection verification
    connected = False
    while connected is not True:
        try:
            connection = urllib.request.urlopen("https://www.google.com.br/").getcode()
            if connection == 200:
                connected = True
            else:
                connected = False
                raise Exception('no connection')
        except (Exception,):
            sleep(20)

    # Make a get request
    response = get('https://www.trabalhabrasil.com.br/vagas-empregos-em-francisco-morato-sp?pagina=' + page)

    # Pause the loop
    sleep(randint(8, 15))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))

    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # Break the loop if the number of requests is greater than expected
    if requests > 5:
        warn('Number of requests was greater than expected.')
        break

    # Parse the content of the request with BeautifulSoup
    soup = bs(response.text, 'html.parser')

    # Select all the 60 jobs containers from a single page
    jobsContainers = soup.find_all('div', class_='jg__container')

    for container in jobsContainers:
        if container.find('div', class_='jg__job') is not None:

            # Scrape city
            cities = soup.select('.job__detail')
            listCity = []
            for city in cities:
                if 'Francisco Morato/SP' in city:
                    listCity.append(city.get_text(strip=True))

            # If the city name change in the page
            if len(listCity) == 0:
                exit()
            else:

                # Scrape title
                titles = soup.select('.job__name')
                listTitle = []
                cont = 0
                for title in titles:
                    if cont < len(listCity):
                        listTitle.append(title.get_text(strip=True))
                        cont += 1

                # Scrape quantity
                quantities = soup.select('.job__name')
                listQuantity = []
                cont = 0
                for quantity in quantities:
                    if cont < len(listCity):
                        listQuantity.append(quantity.get_text(strip=True))
                        cont += 1

                # Scrape company
                cont = 0
                companies = soup.select('.job__company')
                listCompany = []
                for company in companies:
                    if cont < len(listCity):
                        listCompany.append(company.get_text(strip=True))
                        cont += 1

                # Scrape state
                cont = 0
                states = soup.select('.job__detail')
                listState = []
                for state in states:
                    if cont < len(listCity):
                        if 'Francisco Morato/SP' in state:
                            listState.append(state.get_text(strip=True))
                            cont += 1

        # Applyng functions and save in database
        database.savedb(functions.quantity(listQuantity), functions.title(listTitle),
                        functions.company(listCompany), functions.city(listCity),
                        functions.state(listState))
