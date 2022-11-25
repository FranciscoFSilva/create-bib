from habanero import Crossref, WorksContainer
from argparse import ArgumentParser

def get_work(cr,doi,sort = None):
    return cr.works(ids = doi, sort = sort)

def get_authors(work):
    x = WorksContainer(work)
    return x.author[0]

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
            authors = get_authors(work)
            authors_string = get_authors_string(authors)
            print(" ".join(authors_string))
