from fastapi import FastAPI , Path
from typing import Optional
import json


app=FastAPI()
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

@app.get("/search")
def search(last:Optional[str]=None,b_last:Optional[str]=None,count:Optional[int]=None):
    try:
        if last:
            res=json_[last]
            if count:
                res=[i for i in res if len(i)==int(count)]
            if b_last:
                res=[i for i in res if i[-2]==b_last]
            return {"results":res}
        
    except:
        pass
    return {"results":"sothing went wrong"}