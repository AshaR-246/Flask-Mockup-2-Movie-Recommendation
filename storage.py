import csv
all_movies=[]
with open('fin.csv',encoding="utf-8") as f:
    reader=csv.reader(f)
    data=list(reader)
    all_movies=data[1:]
liked_movies=[]
disliked_movies=[]
did_not_watch=[]