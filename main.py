from fastapi import FastAPI , Path
from typing import Optional
from fastapi.responses import HTMLResponse
from db import db


app=FastAPI()
db=db("q2.db")
db.start_connection2()

@app.get("/",response_class=HTMLResponse)
def home():
    return("<p>use <a href='/docs'>docs<a> for help")

@app.get("/data")
def data():
    return {"results":db.rows("select * from words")}

@app.get("/letter/{letter}")
def ltr(letter:str=Path(None,description="arabic letter")):
    try:
        return {"results":db.rows(f"select * from words where last='{str(letter)}'")}
    except:
        return {"results":"something went wrong"}

@app.get("/search")
def search(last:Optional[str]=None,b_last:Optional[str]=None,count:Optional[int]=None):
    try:

        if last:
            if (count and b_last):
                res=db.rows(
                    f"select * from words where last ='{last}' and b_last='{b_last}' and count ={count}")
            elif count:
                res=db.rows(
                    f"select * from words where last ='{last}' and count ={count}")
            elif b_last:
                res=db.rows(
                    f"select * from words where last ='{last}' and b_last='{b_last}'")
            else:
                res=db.rows(f"select * from words where last='{str(last)}'")
            return {"results":res}

        else:
            return {"results":"plz add a last letter"}
    except:
        return {"results":"something went wrong"}

@app.get("/meaning/{word}")
def meaning(word:str=Path(None,description="arabic word")):
    try:
        res=db.rows(f"select meaning from words where word='{word}'")[0]
        if len(res)==1:
            return {"results":res}
        else:
            return {"results":"no such word"}
    except:
        return {"results":"something went wrong"}


@app.get("/copy/{word}")
def copy(word:str=Path(None,description="arabic word")):
    try:
        query=f"""UPDATE words
            SET likes = likes+1
            WHERE word = '{word}';"""
        db.qurey(query)
        return {"resuslts":db.rows(f"select likes from words where word='{word}'")[0]}
    except:
        return {"results":"something went wrong"}
