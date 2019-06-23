import sqlite3
import xlsxwriter
from urllib.request import urlopen
from bs4 import BeautifulSoup
url=input("enter url here\n")
file_handle=urlopen(url)
a=file_handle.read()
try:
    html=urlopen(url)
except HTTPError as e:
    print(e)

soup=BeautifulSoup(a,"html.parser")
for script in soup(["script","style"]):
    script.extract()
text=soup.get_text()
b=text.split()
c=input("enter ur keywords")
usri=c.split()
d={}
for wrd in b:
    for usr in usri:
        if usr==wrd:
            if usr in d:
                d[usr]+=1
            else:
                d[usr]=1
print(d)
conn=sqlite3.connect('mydb1.db')
conn.execute('''create table if not exists wc3(text not null,count int not null)''')
for x,y in d.items():
    conn.execute('''insert into wc3 values(?,?)''',(x,y))
    conn.commit()
tbl=conn.execute("select * from wc3")
for s in tbl:
   print(s)
conn.close()
h=xlsxwriter.Workbook('wordc.xlsx')
r=h.add_worksheet()
row=0
col=0
for p in d.keys():
    r.write(row,col,p)
    row+=1
row=0
col=1
for q in d.values():
    r.write(row,col,q)
    row+=1
data = []    
r.write_column('B1',data)
chart=h.add_chart({'type':'bar'})
chart.add_series({'values':'=sheet1!$B$1:$B$10'})
r.insert_chart('E10',chart)
h.close()
