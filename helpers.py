import os

from bs4 import BeautifulSoup
from collections import Counter
from datetime import date, time, datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from italian_dictionary import get_definition
import spacy
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

languages = ["German", "Italian", "Spanish"]

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code



def lemmatise(text, language):

    #load the correct 
    if language == "Italian":
        
        nlp = spacy.load("it_core_news_sm")
    
    if language == "Spanish":

        nlp = spacy.load("sp_core_news_sm")

    doc = nlp(text)

    lemmas = [token.lemma_ for token in doc]
    return Counter(lemmas)


    
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function



def lookup(wordlist, language):

    if language == "Italian":

        #values is a list of dictionaries where each of the 
        values = {}
        for word in wordlist:

            #use italian dictionary to get the word list
            temp = get_definition(word)

            values[word]["definition"] = temp["definizione"]
            values[word]["part"] = temp["grammatica"]
            return values

    if language == "Spanish":

        #this opens and stores the data from the dictionary xml file
        with open("es-en.xml") as file:

            data = file.read()
        
        #turn file into an xml file to parse
        bs_data = BeautifulSoup(data, "xml")

        #set a dictionary to store all of the collected values
        values = {}

        for word in wordlist:
            
            #find all the entries that match the word
            matching = bs_data.find_all("w", string = word)
            
            #def list is the list of colleccted definitions for the word
            def_list = (row.d.text for row in matching)
            
            #initialise a string to add all the definitions to
            existing = ""
            
            #add each correct definition to this string
            for i in range (len(def_list)):

                existing += f"{ i + 1 }: {def_list[i]} \n"

            #add the definition string and the word to a list
            values[word]["definition"] = existing
            values[word]["part"] = (matching[0].t.text).translate({ord(i) : None for i in '{}'})

        return values
                


def presence(variable, vname):

    if not variable:
        return apology(f"please enter a {vname}")
    
    else:
        return 



def update(db):
        #if new day reset new card counter
    last = db.execute ("SELECT time FROM users WHERE id = ?", session["user_id"])[0]["date"]
    if datetime.date.fromtimestamp(last) != date.today():
        for language in languages:
            session[language]["new_seen"] = 0
            session[language]["reviewed"] = 0
            session[language]["day_start"] = db.execute("""SELECT COUNT (*) FROM user_progress 
            WHERE due < ? AND user_id = ? AND card_id IN 
            (SELECT id FROM cards WHERE language = ?)"""
            , session["datetime"], session["user_id"], language)
        
    #reset time
    session["datetime"] = datetime.now().timestamp()
    #find the number of cards to review
    session[session["language"]]["review_count"] = db.execute("""SELECT COUNT (*) FROM user_progress 
    WHERE due < ? AND user_id = ? AND card_id IN 
    (SELECT id FROM cards WHERE language = ?)"""
    , session["datetime"], session["user_id"], session["language"])
    session["new_cards"] = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["new_cards"]
    #update the time in the database
    db.execute("""UPDATE users SET time = ? WHERE id = ?""", session["datetime"], session["user_id"])
    
    




