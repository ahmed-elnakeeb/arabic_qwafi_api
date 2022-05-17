from fastapi import FastAPI , Path
import pandas as pd
from typing import Optional
import json


app=FastAPI()
df=pd.read_csv("k.csv",encoding="utf-8")
with open('finale.json',encoding="utf_8",mode="r") as json_file:
    json_ = json.load(json_file)

@app.get("/")
def home():
    return("hi")

@app.get("/data")
def data():
    return json_



@app.get("/letter/{letter}")
def ltr(letter:str=Path(None,description="arabic letter")):
    try:
        return {"results":json_[letter]}
    except:
        return ("did not work sorry hazem")

@app.get("/search}")
def search(last:Optional[str]=None,b_last:Optional[str]=None,count:Optional[int]=None):
        result=[]
        if last and (not count) and (not b_last ):
            return ltr(last)
        elif b_last and last and (not count):
            return df.loc[ (df['b_last'] ==b_last) & (df['last'] ==last) ]["words"]
        elif count and last and b_last:
            return df.loc[ (df['b_last'] ==b_last) & (df['last'] ==last)&(df['count'] ==count)   ]["words"]
        elif count and last:
             return df.loc[(df['last'] ==last)&(df['count'] ==count)   ]["words"]
        elif count:
            return df.loc[(df['count'] ==count)   ]["words"]
        return {"results":"sothing went wrong "}
