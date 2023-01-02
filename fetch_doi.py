import requests
from bs4 import BeautifulSoup

request = requests.get('https://www.mdpi.com/1996-1073/14/21/6861')


soup = BeautifulSoup(request.content, 'html.parser')

section = soup.find('section', id="html-references_list") 
ordered_list = section.find('ol')
lists = ordered_list.find_all('li')

with open('doi_intro.txt', 'w') as output:
    for list in lists:
        hyperlink = list.find('a', class_="cross-ref")
        if hyperlink is not None:
            href = hyperlink.get('href')
            output.write(f"{href}\n")
