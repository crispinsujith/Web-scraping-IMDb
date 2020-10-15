import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from time import sleep
from random import randint

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

url1="https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
response=requests.get(url1)
soup1=BeautifulSoup(response.content,"lxml")
body=soup1.select("div.lister.list.detail.sub-list")[0]
indivs=body.select("div.lister-item.mode-advanced")
name=[i.select("h3.lister-item-header")[0].get_text().strip().replace("\n","")[2:].replace(".","")[:-6].replace("(I)","").replace("(II)","").replace("(III)","") for i in indivs]
para=[i.select("p.text-muted")[1].get_text().strip() for i in indivs]
rating=[i.select("div.inline-block.ratings-imdb-rating strong")[0].get_text() for i in indivs]
pages=np.arange(51,1001,50)
para1=[]
name1=[]
rating1=[]
for i in pages:
    link="https://www.imdb.com/search/title/?groups=top_1000&start={i}&ref_=adv_nxt".format(i=i)
    response=requests.get(link)
    soup=BeautifulSoup(response.content,"lxml")
    body=soup.select("div.lister.list.detail.sub-list")[0]
    indivs=body.select("div.lister-item.mode-advanced")
    sleep(randint(2,6))
    for i in indivs:
        name1.append(i.select("h3.lister-item-header")[0].get_text().strip().replace("\n","")[3:].replace(".","")[:-6].replace("00","").replace("(I)","").replace("(II)","").replace("(III)",""))
        para1.append(i.select("p.text-muted")[1].get_text().strip())
        rating1.append(i.select("div.inline-block.ratings-imdb-rating strong")[0].get_text())
final_name=name+name1
final_para=para+para1
final_rating=rating+rating1
df=pd.DataFrame({"Movie Name":final_name,"IMDB Rating":final_rating,"Movie Summary":final_para},index=[indexx for indexx in range(1,len(final_name)+1)])
df.to_csv("imdb_full_list.csv")
df
