from flask import Flask, request
from helpers.mongoConnection import read, insert
from bson import json_util, ObjectId
from helpers.checking import check_mandatory, check_groups

app = Flask("starwarsquotes")


@app.route("/salute")
def sayhi():
    return "May the Force be with you"

@app.route("/quotes/new")
def celebrities_new():
    args = dict(request.args)
    if not check_mandatory(args,["name", "army", "movie", "quote"]):
        return {"Error":"missing obligatory parameter"}


    if not check_groups(args,"army",["Rebellion", "Empire", "Bounty hunters"]):
        return {"Error":"You have to chose between Rebellion, Empire and Bounty hunters"}
    if not check_groups(args,"movie",["A New Hope", "The Empire Strikes Back", "Return of the Jedi"]):
        return {"Error":"Not a Star Wars Movie"}

    q = {"quote":args["quote"]}
    data = read(q)
    if len(data)>0:
        return {"Error":"The sentence is already in the list"}

    res = insert(args)
    return json_util.dumps({"_id":res})


@app.route("/quotes/all")
def all_quotes():
    data = read({}, project={"name":1, "quote":1, "_id":0})
    return json_util.dumps(data)


@app.route("/quotesbyarmy/<army>")
def quotes_by_army(army):
    q = {"army":army}
    if not check_groups(q,"army",["Rebellion", "Empire", "Bounty hunters"]):
        return {"Error":"You have to chose between Rebellion, Empire and Bounty hunters"}
    data = read(q, project={"name":1, "quote":1, "_id":0})
    return json_util.dumps(data)


@app.route("/quotesbycharacter/<character>")
def quotes_by_character(character):
    q = {"name":character}
    data = read(q, project={"name":1, "quote":1, "_id":0})
    if len(data) == 0:
        return {"Error":"The character is still not in the Database"}
    return json_util.dumps(data)

@app.route("/quotesbymovie/<movie>")
def quotes_by_movie(movie):
    q = {"movie":movie}
    if not check_groups(q,"movie",["A New Hope", "The Empire Strikes Back", "Return of the Jedi"]):
        return {"Error":"The movie is still not in the database"}
    data = read(q, project={"name":1, "quote":1, "_id":0})

    return json_util.dumps(data)

app.run(debug=True)