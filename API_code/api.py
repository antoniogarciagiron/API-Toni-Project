#api.py is the principal file, connects the API and defines API enpoints

from flask import Flask, request
from helpers.mongoConnection import read, insert
from bson import json_util, ObjectId
from helpers.checking import check_mandatory, check_groups

app = Flask("starwarsquotes")


@app.route("/salute")
def sayhi():
    '''
    Endpoint to test the API and say "hi" to the user 
    Takes: -
    Returns: a default sentence to salute
    '''
    return "May the Force be with you"

@app.route("/quotes/new")
def quotes_new():
    '''
    Endpoint to insert a new field into the database through the API. Checks if the arguments are correct before inserting
    Takes: a dictionary with the fields to insert, i.e. "name", "army", "movie" and "quote"
    Returns: the object ID if the arguments are correct. Otherwise returns an error
    '''
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
    '''
    Endpoint to return all the quotes
    Takes: -
    Returns: a json with all the StarWars quotes into the dataset and the author of the quote
    '''
    data = read({}, project={"name":1, "quote":1, "_id":0})
    return json_util.dumps(data)


@app.route("/quotesbyarmy/<army>")
def quotes_by_army(army):
    '''
    Endpoint to return all the quotes by affiliation
    Takes: the affiliation, i.e. Rebellion, Empire or Bounty hunters
    Returns: a json with all the StarWars quotes into the dataset and the author of the quote for the selected affiliation(army). If the affiliation is not included, returns an error
    '''
    q = {"army":army}
    if not check_groups(q,"army",["Rebellion", "Empire", "Bounty hunters"]):
        return {"Error":"You have to chose between Rebellion, Empire and Bounty hunters"}
    data = read(q, project={"name":1, "quote":1, "_id":0})
    return json_util.dumps(data)


@app.route("/quotesbycharacter/<character>")
def quotes_by_character(character):
    '''
    Endpoint to return all the quotes by character
    Takes: name of the character
    Returns: a json with all the StarWars quotes into the dataset for the chosen character. If the character is not included, returns an error
    '''
    q = {"name":character}
    data = read(q, project={"name":1, "quote":1, "_id":0})
    if len(data) == 0:
        return {"Error":"The character is still not in the Database"}
    return json_util.dumps(data)

@app.route("/quotesbymovie/<movie>")
def quotes_by_movie(movie):
    '''
    Endpoint to return all the quotes by SW movie
    Takes: name of the movie
    Returns: a json with all the StarWars quotes into the dataset for the chosen movie. If the movie is not included, returns an error
    '''
    q = {"movie":movie}
    if not check_groups(q,"movie",["A New Hope", "The Empire Strikes Back", "Return of the Jedi"]):
        return {"Error":"The movie is still not in the database"}
    data = read(q, project={"name":1, "quote":1, "_id":0})

    return json_util.dumps(data)

app.run(debug=True)