import twint
import os
import csv
from threading import Thread
import asyncio


def load_csv(file):
    rows = []
    with open(file, newline='',encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows

class Search(Thread):
    def __init__(self, file, keyword=None, to_username=None, from_username=None, allow_append=False):
        self.file = file
        self.keyword = keyword
        self.to_username = to_username
        self.from_username = from_username
        self.allow_append = allow_append
        Thread.__init__(self)

    def run(self):
        print("New search launched : \n keyword: {}\n to: {}\n from: {}\n file:  {}\n".format(self.keyword, self.to_username, self.from_username, self.file))

        # création de l’objet twint
        c = twint.Config()
        # Critères de recherche
        if self.keyword:
            c.Search = self.keyword
        if self.to_username:
            c.To = self.to_username
        if self.from_username:
            c.Username = self.from_username

        ##Exemple of query : from WholeFoods to IIMiranda
        # c.To = "IIMiranda"
        # c.Username = "WholeFoods"

        # Champs à stocker dans le CSV
        # c.Custom["tweet"] = ["tweet"]

        c.Store_csv = True
        c.Count = True
        c.Hide_output = True
        c.Output = self.file

        if (not self.allow_append) and os.path.exists(self.file):
            print("Cancelled search : file already existing : {}".format(self.file))
        else:
            asyncio.set_event_loop(asyncio.new_event_loop())
            twint.run.Search(c)
            print("Search done")


def extract_service_clients_data():
    #Load csv with account names + filenames
    brands = load_csv('D:/Centrale 3A/OSY/Data Science/repos/observatoire-twitter/extraction_twint/brand_accounts.csv')

    #Launch a search for every brand, and store it in the appropriate file
    for brand in brands:

        #set up the search
        filename = "D:/Centrale 3A/OSY/Data Science/repos/observatoire-twitter/extraction_twint/data_service_clients/" + brand.get("filename") + ".csv"
        search=Search(filename, keyword=brand["account"])
        #start the search
        search.start()


def extract_marketing_personnalise_data():
    #Load csv with account names + filenames
    products = [product.get('product') for product in load_csv('D:/Centrale 3A/OSY/Data Science/repos/observatoire-twitter/extraction_twint/product_keywords.csv')]

    #Launch a search for every brand, and store it in the appropriate file
    for product in products:
        print(product)

        #set up the search
        filename = "D:/Centrale 3A/OSY/Data Science/repos/observatoire-twitter/extraction_twint/data_marketing_personnalise/" + product + ".csv"
        search=Search(filename, keyword=product)
        #start the search
        search.start()


if __name__=="__main__":

    extract_service_clients_data()
    extract_marketing_personnalise_data()








