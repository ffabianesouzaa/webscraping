import re


# Removing numbers of the title
def title(titles):
    jobTitle = []
    for title in titles:
        pattern = r'[0-9]\s*'
        newTitle = re.sub(pattern, '', title)
        jobTitle.append(newTitle)

    return jobTitle


# Removing letters of the title
def quantity(quantities):
    jobQuantity = []
    for quantity in quantities:
        pattern = r'[^0-9]'
        newJob = re.sub(pattern, '', quantity)
        jobQuantity.append(newJob)

    # Filling empty spaces with 1
    jobQuantityAll = []
    for quantity in jobQuantity:
        if quantity == '':
            quantity = '1'
            jobQuantityAll.append(quantity)
        else:
            jobQuantityAll.append(quantity)

    return jobQuantityAll


# Removing '()' from name companies
def company(companies):
    jobCompany = []
    for company in companies:
        pattern = r'[()]+'
        newCompany = re.sub(pattern, '', company)
        jobCompany.append(newCompany)

    return jobCompany


# Removing salary informations
def city(cities):
    jobCity = []
    for city in cities:
        if city.count('R$') == 1:
            del (city)
        else:
            jobCity.append(city)

    # Separing city and state
    jobCityAux = []
    for city in jobCity:
        jobCityAux.append(city.split('/'))

    # Unpacking list
    output = []

    def unpackList(l):
        for item in l:
            if type(item) == list:
                unpackList(item)
            else:
                output.append(item)

    unpackList(jobCityAux)

    # Add city name in a list
    jobCityAll = (output[::2])

    return jobCityAll


# Removing salary informations
def state(states):
    jobState = []
    for state in states:
        if state.count('R$') == 1:
            del (state)
        else:
            jobState.append(state)

    # Separing city and state
    jobStateAux = []
    for state in jobState:
        jobStateAux.append(state.split('/'))

    # Unpacking list
    output = []

    def unpackList(l):
        for item in l:
            if type(item) == list:
                unpackList(item)
            else:
                output.append(item)

    unpackList(jobStateAux)

    # Add state name in a list
    jobStateAll = (output[::-2])

    return jobStateAll
