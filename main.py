from titlecase import titlecase
from habanero import Crossref, WorksContainer
from argparse import ArgumentParser
import csv

def get_work(cr,doi,sort = None):
    return cr.works(ids = doi, sort = sort)

def get_authors(work):
    x = WorksContainer(work)
    return x.author[0]

def get_title(work):
    x = WorksContainer(work)
    return x.title[0]

def get_authors_string(authors):
    noAuthors = len(authors)
    stringList = [""]*(2*noAuthors-1)
    stringList[1::2] = ["and"]*(noAuthors-1)
    idx = 0
    for author in authors:
        given = ""
        family = ""
        if "given" in author:
            given = author["given"]
        if "family" in author:
            family = author["family"]
        stringList[idx] = family + ", " + given
        idx +=2
    return stringList

def get_first_author(authors):
    for author in authors:
        if "sequence" in author:
            if author["sequence"] == "first":
                return author["family"]
    return ""

def get_published_date(work):
    x = WorksContainer(work)
    if hasattr(x, "published_print"):
        published_print = x.published_print
        date = published_print[0]
        return date["date-parts"][0]
    return []

def get_year(date):
    return date[0]

def get_month(date):
    if len(date) >= 2:
        return date[1]
    return 0

if __name__ == "__main__":
    mailto = "francisco.ferreira.silva@tecnico.ulisboa.pt"
    cr = Crossref(mailto = mailto)
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="myFile", help="Open specified file")
    args = parser.parse_args()
    myFile = args.myFile
    article_info_list  = []
    with open(myFile) as file:
        data = file.read()
        data_list = data.split("\n")
        works = get_work(cr,data_list)
        for work in works:
            date = get_published_date(work)
            authors = get_authors(work)
            title = get_title(work)
            first = get_first_author(authors)
            authors_string = get_authors_string(authors)
            if not date:
                year = 0
                month = 0
            else:
                year = get_year(date)
                month = get_month(date)
            article_info_list.append({'year': year, 'month': month, 'first': str.title(first), 'authors': titlecase(' '.join(authors_string)), 'title': titlecase(title[0])})

    csv_filename = 'bib.csv'
    fields = ['year', 'month', 'first', 'authors', 'title']
    with open(csv_filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        writer.writerows(article_info_list)
