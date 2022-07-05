from db import db
import json


dbm=db("qafia.db")
with open('finale.json',encoding="utf_8",mode="r") as json_file:
    json_ = json.load(json_file)

# query="""
#     CREATE TABLE IF NOT EXISTS words (
#     id integer PRIMARY KEY,
#     word text NOT NULL unique,
#     copied int default 0,
#     meaning text default ''
#         );
# """

dbm.start_connection()


# for key, value in json_.items():
#     for i in value:
#         query=f"""insert into words(word) values('{str(i)}')"""
#         dbm.qurey(query)


query="""select * from words"""
print(len(dbm.rows(query)))
dbm.stop_connection()