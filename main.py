from habanero import Crossref, WorksContainer

def get_work(cr,doi):
    return cr.works(ids = doi)

def get_authors(work):
    x = WorksContainer(work)
    return x.author[0]

def get_authors_string(authors):
    noAuthors = len(authors)
    stringList = [""]*(2*noAuthors-1)
    stringList[1::2] = ["and"]*(noAuthors-1)
    idx = 0
    for author in authors:
        given = author["given"]
        family = author["family"]
        stringList[idx] = family + ", " + given
        idx +=2
    return stringList

if __name__ == "__main__":
    mailto = "francisco.ferreira.silva@tecnico.ulisboa.pt"
    cr = Crossref(mailto = mailto)
    work = get_work(cr,"10.3390/en14216861")
    authors = get_authors(work)
    authors_string = get_authors_string(authors)
    print(" ".join(authors_string))

