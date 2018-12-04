from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl
import codecs

#ignore ssl certifications
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

word = input("What do you want to search? ")
word = word.strip()
word = word.replace(' ','+')
if len(word) < 1: word = 'Monuments'
url='https://en.wikipedia.org/w/index.php?title=Special:Search&limit=100&offset=0&ns0=1&search='+word+'&advancedSearch-current={%22namespaces%22:[0]}'

data = urllib.request.urlopen(url, context=ctx).read().decode()
soup = BeautifulSoup(data, 'html.parser')
lists = (soup.find_all('ul', {'class':'mw-search-results'}))[0].find_all('li')

fh = codecs.open("View.js", 'w', 'utf-8')
fh.write("myData = [\n")
i = 1
for list in lists:
    tag = list('a')
    id = i
    title = tag[0]['title']
    link = "https://en.wikipedia.org"+tag[0]['href']
    print(id, title, link, "\n")
    fh.write('''['''+str(id)+''',"'''+title+'''","'''+link+'''"],\n''')

    i = i+1
fh.write('''];

function link() {
myData.forEach(myFunc);
}

function myFunc(value) {
document.write("<tr><td>"+value[0]+"</td><td>"+value[1]+"</td><td><a href='"+value[2]+"'>"+value[2]+"</a></td></tr>");
}
''')
fh.close
