from fastapi import FastAPI, Path
from typing import Optional
from fastapi.responses import HTMLResponse
from db import db
from fastapi.middleware.cors import CORSMiddleware
import csv
import json
from tools import get_templates
from functools import cache
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/", StaticFiles(directory="static",html = True), name="static")



origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = db("el-qafia.db")
db.start_connection2()


@app.get("/", response_class=HTMLResponse)
def home():
    return("<p>use <a href='/docs'>docs<a> for help")

@app.get("/data")
def data():
    return {"results": db.rows("select * from words")}

@cache
@app.get("/letter/{letter}")
def ltr(letter: str = Path(None, description="arabic letter")):
    try:
        return {"results": db.rows(f"select word,id from words where last='{str(letter)}' order by count desc")}
    except:
        return {"results": "something went wrong"}

@cache
@app.get("/search_word")
def search_word(word: Optional[str] = None):

    templates=get_templates(word)
    results=[]
    try:    
        for _template in templates:
            print("template", _template)
            query = f"select word,id from words where word like '{_template}'  order by count desc "
            res = db.rows(query)
            results+= res
        results=list(dict.fromkeys(results))
        return {"results": results}

    except:
        return {"results": "something went wrong"}


@app.get("/search")
def search(first: Optional[str] = None, last: Optional[str] = None, b_last: Optional[str] = None, size: Optional[int] = None, min: Optional[int] = 0, max: Optional[int] = 100):
    try:
        if last:
            if (size and b_last):
                res = db.rows(
                    f"select word,id from words where last ='{last}' and b_last='{b_last}'  and size ={size} order by count desc ")
            elif size:
                res = db.rows(
                    f"select word,id from words where last ='{last}' and size ={size} order by count desc")
            elif b_last:
                res = db.rows(
                    f"select word,id from words where last ='{last}' and b_last='{b_last}' and size  BETWEEN {min} and {max} order by count desc")
            else:
                res = db.rows(
                    f"select word,id from words where last='{str(last)}' and size  BETWEEN {min} and {max} order by count desc")
            return {"results": res}

        else:
            return {"results": "plz add a last letter"}
    except:
        return {"results": "something went wrong"}

@cache
@app.get("/mostliked")
def mostliked():
    query = "select word,id from words order by count desc limit 1000"
    rows = db.rows(query)
    return {"results": rows}


@app.get("/meaning")
def meaning(word: Optional[str] = None, words: Optional[str] = None, id: int = None, ids: str = None):
    # try:
    res = []

    if id:
        res = [db.rows(f"select meanings from words where id={id}")]

    elif word:
        res = [
            db.rows(f"select meanings from words where word='{word}'")[0][0]]
    elif words:
        words = [str(w) for w in words.split()]
        print(words)
        for word in words:
            res.append(
                db.rows(f"select meanings from words where word='{word}'")[0][0])
    elif ids:
        ids = [int(i) for i in ids.split()]
        for id in ids:
            res.append(
                db.rows(f"select meanings from words where id='{id}'")[0][0])
    if len(res) >= 1:
        return {"results": res}
    else:
        return {"results": "no such word"}
    # except:
    #     return {"results": "something went wrong"}


@app.get("/quote")
def quote():
    from tools import dayOfYear

    day = dayOfYear()
    with open('quotes.csv', newline='', encoding="utf-8-sig") as f:
        data = list(csv.reader(f))
        return(data[day])


@app.get("/info")
def info(id: int = None, word: str = None):
    if id:
        return(
            db.rows(f"select * from words where id='{id}'"))

    elif word:
        return(
            db.rows(f"select * from words where word='{word}'"))


@app.post("/comment")
def comment(comment: str, user: Optional[str] = None, section: Optional[str] = None):
    try:
        if user and section:
            query = f"insert into comments (user,comment,section) values('{user}','{comment}','{section}') "
            db.qurey(query)

        elif section:
            query = f"insert into comments (comment,section) values('{comment}','{section}') "
            db.qurey(query)
        elif user:
            query = f"insert into comments (user,comment) values('{user}','{comment}') "
            db.qurey(query)
        else:
            query = f"insert into comments (comment) values('{comment}') "
            db.qurey(query)
        return {"results": "accepted"}
    except:
        return {"results": "something went wrong"}


@app.get("/comments")
def comments(section: Optional[str] = "global"):
    query = f"select * from comments where section='{section}'"
    return {"results": db.rows(query)}


@app.post("/add_qafia")
def add_qafia(qafia: str, meaning: str = None):
    with open("temp.txt", encoding="utf-8", mode="a") as file:
        file.write(f"{qafia},{meaning}\n")

def main():
    import uvicorn
    uvicorn.run(app, host="192.168.1.100", port=8000)

if __name__ == "__main__":
    main()