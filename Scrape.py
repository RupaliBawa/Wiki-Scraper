from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl
import re
import random
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

titles = []
fh = codecs.open("View.js", 'w', 'utf-8')
fh.write("myData = [\n")
i = 1
for list in lists:
    tag = list('a')
    id = i
    title = tag[0]['title']
    link = "https://en.wikipedia.org"+tag[0]['href']
    print(id, title, link, "\n")
    titles.append(title)
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

print(titles)

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20
#counts = [*range(10,60,4)]
regex = re.compile("[!@#$%^&*()_+-=?<>:'|\/.,;`~]")

fhand = open('word.js','w')
fhand.write("gword = [")
first = True
i=0
for k in titles:
    if regex.search(k) != None: continue
    if not first : fhand.write( ",\n")
    first = False
    #size = counts[k]
    #size = (size - lowest) / float(highest - lowest)
    #size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(random.randrange(10,50,4))+"}")
    #i=i+1
    #if(i>90): i=50
fhand.write( "\n];\n")
fhand.close()
