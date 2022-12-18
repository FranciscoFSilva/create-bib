import time
from habanero import Crossref, WorksContainer
from argparse import ArgumentParser

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

if __name__ == "__main__":
    mailto = "francisco.ferreira.silva@tecnico.ulisboa.pt"
    cr = Crossref(mailto = mailto)
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="myFile", help="Open specified file")
    args = parser.parse_args()
    myFile = args.myFile
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
            authors_string = get_authors_string(authors)
            if not date:
                date = [0]
            text = f"{' '.join(map(str,date))} - {' '.join(authors_string)}: {title[0]}."
            print(text)
