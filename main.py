import json
import psycopg2
from psycopg2 import sql
import dateutil.parser
import configparser

print("|| Opening config file...")
config = configparser.ConfigParser()
config.read("./config.ini")


print("|| Opening json file...")
with open('result.json', 'r', encoding='utf-8') as garbage:
    imported_data = json.load(garbage)

print("===============================================")
print("CHAT INFO\n ")
print("Chat Name:\t", imported_data["name"])
print("Chat Type:\t", imported_data["type"])
print("Chat ID:\t", imported_data["id"])
print("===============================================")

def fixtext(oldtext):

    fixedtext = []

    if type(oldtext) is list:

        for cursedtextobject in oldtext:
            if type(cursedtextobject) is dict:
                fixedtext.append(cursedtextobject["text"])

            else:
                fixedtext.append(cursedtextobject)
    

    else:
        fixedtext.append(oldtext)

   
    betterfixedtext = ""

    for dingle in fixedtext:
        betterfixedtext = betterfixedtext + dingle

    return betterfixedtext

def fixtimestamp(oldtimestamp):
    print(dateutil.parser.parse(oldtimestamp))
    return dateutil.parser.parse(oldtimestamp)

print("|| Connecting to Postgres...")
conn = psycopg2.connect(
    database=config["db"]["database"],
    user=config["db"]["user"],
    password=config["db"]["password"])

c = conn.cursor()

messages = imported_data["messages"]

print("|| Processing messages...")

for message in messages:

    # Handle regular text messages
    if message["type"] == "message":

        newtext = fixtext(message["text"]) # strip formatting information inside text. maybe someday we won't do that?
        newtimestamp = fixtimestamp(message["date"]) # convert telegram timestamp to python object, so that psycopg2 can convert it to a postgres timestamp

        width = 0
        height = 0

        if 'width' in message:
            width = message["width"]
        else:
            width = None

        if "height" in message:
            height = message["height"]
        else:
            height = None

        #need to use the SQL object here from psycopg2 so we can pass in the table name - this should avoid sql injection (which i mean isn't a big deal for this but hey, best practices right?)
        query = sql.SQL("INSERT INTO {} (id, type, date, \"from\", from_id, text, height, width) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ON CONSTRAINT {}_pkey DO NOTHING;".format(config["db"]["table"],config["db"]["table"])) 
        c.execute(query,(message["id"], message["type"], newtimestamp, message["from"], message["from_id"], newtext, height, width))


conn.commit()
