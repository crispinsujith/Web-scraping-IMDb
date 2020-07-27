import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import pdb
start_time=time.time()
response=requests.get("https://www.imdb.com/chart/top/")
soup = BeautifulSoup(response.content,"lxml")
body=soup.select("tbody.lister-list")[0]
titles=[]
ratings=[]
summ=[]
for row in body.select("tr"):
    title=row.select("td.titleColumn a")[0].get_text().strip()
    titles.append(title)
    rating=row.select("td.ratingColumn.imdbRating")[0].get_text().strip()
    ratings.append(rating)
    innerlink=row.select("td.posterColumn a")[0]["href"]
    link="https://imdb.com"+innerlink
    #pdb.set_trace()
    response2=requests.get(link).content
    soup2=BeautifulSoup(response2,"lxml")
    summary=soup2.select("div.summary_text")[0].get_text().strip()
    summ.append(summary)
df=pd.DataFrame({"Title":titles,"IMDB Rating":ratings, "Movie Summary":summ})
df.to_csv("imdbmovies.csv")
end_time=time.time()
finish=end_time-start_time
print("Runtime is {f:1.4f} secs".format(f=finish))
print(df)
