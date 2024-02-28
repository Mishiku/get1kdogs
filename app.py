import requests
import sqlite3

def getPageresults(index):

    site_url = f'https://geoapi.freeimages.com/istock/search/?phrase=dogs&page={index}&page_size=100&graphical_styles=photography&lang=en-US'

    x = requests.get(site_url)

    urls = []
    #use the format of the http response to our advantage
    results = x.json()['data']['results']

    #Looking at the http response, I'll take the picture with the highest res
    for pic in results:
        for size in pic['display_sizes']:
            if size['name'] == 'high_res_comp':
                urls.append(size['uri'])
                break

    return urls


def loopPages():
    allpics = []
    for i in range(1,11):
        x = getPageresults(i)
        for contents in x:

            allpics.append([contents])
    return allpics
        
#database conn
conn = sqlite3.connect('dogs.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS dogs (url text PRIMARY KEY)')

#I'll use the http request the page does to retrieve the results from a page
# the page can only display up to 100 results per page, so for 1000 dogs we'll have to cycle 100 results 10 times:
results = loopPages()

#Insert to the db only new values
cur.executemany('INSERT OR IGNORE INTO dogs VALUES (?)',results)
conn.commit()


