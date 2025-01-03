import os

from datetime import date, time, datetime, timestamp, fromtimestamp, deltatime
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, presence

app = flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect("languagecards.db")
db = con.cursor()

@app.route("/")
@login_required
def index():

    update()
    
    decks = db.execute(
    """SELECT * FROM decks JOIN users_to_decks ON decks.id = users_to_decks.deck_id 
    WHERE user_id = ? AND decks.language = ?"""
    , session["user_id"], session["language"])
    for deck in decks:
        known = db.execute("""SELECT COUNT (*) FROM user_progress WHERE state = known AND user_id = ? 
        AND card_id IN (SELECT card_id FROM deck_contents WHERE deck_id = ?)""",
        session["user_id"], deck["decks.id"])
        db.execute("UPDATE users_to_decks SET progress = ? WHERE deck_id = ? AND user_id = ?", known/deck["decks.size"], deck[decks.id], session["user_id"])
    order = db.execute ("SELECT deck_order FROM settings WHERE user_id = ?")[0]["deck_order"]
    display =  db.execute("SELECT * FROM decks JOIN decks ON decks.id = users_to_decks.deck_id WHERE users_to_decks.user_id = ? ORDER BY ?", session["user_id"], order)

    

    return render_template ("mainpage.html", display = display)



@app.route("/deck")
@login_required
def deck():

    

@app.route("/new_deck" methods = ["GET", "POST"])
@login_required
def new_deck()
    
    if request.method == POST:
        #get the required variables from the form
        language = request.form.get ("language")
        presence(language, "language")
        if language != session["language"]:
            session["language"] = language
            db.execute("UPDATE users SET language = ? WHERE id = ?", language, session["user_id"])
        name = request.form.get("name")
        presence(name, "name")
        medium = request.form.get("medium")
        genre = request.form.get("genre")
        author = request.form.get("author")
        date = request.form.get("date")
        #use the decks table to enter this data
        db.execute("INSERT INTO decks (language, name, medium, genre, author, date) VALUES (?,?,?,?,?,?)", language, name, medium, genre, author, date)
        session["deck_id"] = db.execute("SELECT id FROM decks WHERE name = ?", name)[0]["name"]
        return redirect ("/input")

    else: 
        return render_template("new_deck.html")



@app.route("/input", methods=["POST"])
@login_required
def input():

    ### TODO: Make a duplicate deck when a deck is updated, rather than updating the whole deck

    #display the npage
    if not input_type:
        return render_template("input.html", deck = deck)
    
    # if a file is inputted, read it into a variable, split the string into a list of words
    if input_type == f:
        with open (request.form.get("input")) as file:
            reader = file.read()
            wordlist = split(reader)
    if input_type == t:
        wordlist = split(request.form.get("input"))

    # lemmatise each word and get a list of words and their frequencies
    lemmas = []
    for word in wordlist:
        lemmas["word"] = lemma(word)
    new = lemmas.counter()

    # create list of all words that have been created already 
    existing = []
    created = db.execute("SELECT * FROM words WHERE language = ?", session["language"])
    for word in created:
        existing.append(created[word]["word"])
    
    #create a list of all words in this deck
    deck_words = db.execute("""SELECT word_id FROM deck_contents WHERE deck_id = ?""", session["deck_id"])
    contents = []
    for word in deck_words:
        contents.append(deck_words[word]["word_id"])
    
    #create a list of the user's words
    uwords = db.execute("""SELECT word_id FROM user_progress WHERE user_id = ? AND language = ?""", session["user_id"], session['language'])
    user_words = []
    for word in uwords:
        user_words.append(uwords[word]["word_id"])

    #for each word, if it is new create a card. 
    uncommon = []
    
    for word in new:
        if word not in existing:
            values = lookup(word)

            #if data cannot be found it is an uncommon word, store for later
            if not json["translation"]:
                uncommon.append(word)
            db.execute ("""INSERT INTO words (word, language, definition, frequency, part, common) 
            VALUES(?,?,?,?,?,common)""" word, session["language"], values["definition"], values["frequency"], values["part"])

        # TODO: rework deck updates
        # if the word is not in this deck, add it to the deck
        word_id = db.execute ("SELECT id FROM words WHERE word = ?", word)[0]["id"]
        if word_id not in contents:
            db.execute("INSERT INTO deck_contents (deck_id, word_id, frequency) VALUES (?,?,?)" deck_id, word_id, cards[word])
        # if the word is in the deck, add the frequency value
        else:
            frequency = db.execute ("SELECT frequency FROM deck_contents WHERE word_id = ?", word_id)[0]["frequency"] + cards[word]
            db.execute ("UPDATE deck_contents SET frequency = ? WHERE word_id = ?", frequency, word_id)
        
        # add the card to user_progress or update frequency
        if word_id not in user_words:
            db.execute ("""INSERT INTO user_progress 
            (user_id, word_id, viewings, easy, good, ok, some, none, state, frequency) VALUES
            (?,?,0,0,0,0,0,0,new,?)""", session["user_id"], word_id, new[word])
        else:
            frequency = db.execute("""SELECT frequency FROM user_progress WHERE user_id = ? AND word_id = ?""",
            session["user_id"], word_id)[0]["frequency"] + new[word]
            db.execute("""UPDATE user_progress SET frequency = ? WHERE user_id = ?, word_id = ?""", frequency, session["user_id"], word_id)



@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == POST:

        # check that username and password have been entered
        username = request.form.get("username")
        presence (username, "username")
        password = request.form.get("password")
        presence (password, "password")

        # check that these values are correct
        rows = db.execute("SELECT * FROM users WHERE username = ?")

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("incorrect username and or password", 403)
        
        # create session with the person's id, storing other key settings
        session["user_id"] = rows[0]["id"]
        session["language"] = rows[0]["language"]
        session["deck_order"] = rows[0]["deck_order"]
        session["card_order"] = rows[0]["card_order"]

        return redirect("/")             

    #if method is GET, render the login form
    else:
        return render_template("login.html")


    
@app.route("/logout")
@login_required
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == POST:
        # check that a username password and confirmation have been entered
        username = request.form.get("username")
        presence (username, "username")
        password = request.form.get("password")
        presence (password, "password")
        confirm = request.form.get("confirm")
        presence (confirm, "confirmation")

        # check that password and username are valid
        if password != confirm:
            return apology("confirmation does not match password", 403)
        check_username = db.execute("SELECT COUNT (*) FROM users WHERE username = ?", username)
        if check_username == 1:
            return apology("This username is already taken", 403)
        
        # input new user into database
        db.execute ("INSERT INTO users (username, hash) VALUES (?,?)", username, generate_password_hash(password))
        return redirect ("/")

    else:
        return render_template ("register.html")


@app.route("/review", methods=["GET", "POST"])
@login_required
def review():
    
    if request.method == POST:

        #reset time
        update()

        #get the value of multiplier
        multiplier = request.form.get("multiplier")

        #get the last interval
        interval = db.execute("SELECT interval FROM user_progress")[0]["interval"]

        #if interval is longer than a day, do the maths
        if interval >= 86400:
            if multiplier > 0:
                interval *= multiplier
                if interval < 86400:
                    interval = 86400
            else interval = 600

            if multiplier != 0.05:
                due = interval + session["datetime"]
            else:
                due = 900 + session["datetime"]

        #if not, use the preset values for short periods
        else: 
            if multiplier = 0:
                interval = 600
            elif multiplier = 0.05:
                interval = 43200
            elif multiplier = 1:
                interval = 86400
            elif multiplier = 2:
                interval = 345600
            else:
                interval = 846000
            due =  interval + session["datetime"]

        # update the database with this data
        viewings = db.execute ("SELECT * FROM user_progress WHERE user_id = ? AND word_id = ?", session["user_id"], session["card"])[0]
        db.execute("""UPDATE user_progress SET due = ? seen = ? interval = ? viewings = ?
        WHERE user_id = ? AND word_id = ?""", due, session["datetime"], interval, viewings["viewings"] + 1, session["user_id"], session["card"])
        value = db.execute("SELECT * FROM ")
        if multiplier = 0:
            db.execute("""UPDATE user_progress SET none = ? WHERE user_id = ? AND card_id = ?"""
            , viewings["none"] + 1, session["user_id"], session["card"])
        elif multiplier = 0.05:
        elif multiplier = 1:
        elif multiplier = 2:
        elif multiplier = 3:

        
        
            


    else:

        update()
        #decide what the next card to show is and display it

        #if the reviewed percentage is greater than the new percentage, show a new card
        #TODO: make the counts for each language independent
        if session["new_seen"]/session["new_cards"] < session["reviewed"]/session["review_count"] AND session["new_seen"]:
            card = db.execute ("""SELECT * FROM user_progress 
            JOIN words ON user_progress.word_id = words.id 
            WHERE user_progress.user_id = ? AND user_progress.state = new AND card_id IN 
            (SELECT card_id FROM deck_contents WHERE deck_id = ?)
             ORDER BY ? LIMIT 1""", session["user_id"], session["deck_id"], session["order"])

        #if possible, choose the longest overdue card with interval < 1 hr
        else:
            card = db.execute ("""SELECT * FROM user_progress 
            JOIN words ON user_progress.word_id = words.id 
            WHERE user_progress.user_id = ? AND user_progress.state = seen AND words.language = ? 
            AND user_pogress.due < ? AND user_progress.interval < 3600
            ORDER BY due LIMIT 1""", session["user_id"], session["language"], datetime.now())

            # if there is no short interval card, choose long interval card
            if not card:
                card = db.execute ("""SELECT * FROM user_progress 
                JOIN words ON user_progress.word_id = words.id 
                WHERE user_progress.user_id = ? AND user_progress.state = seen AND words.language = ? 
                AND user_pogress.due < ? 
                ORDER BY due LIMIT 1""", session["user_id"], session["language"], datetime.now())
        
        # if there are any short interval cards to review, do so before ending the session
        if not card:
            card = db.execute ("""SELECT * FROM user_progress 
            JOIN words ON user_progress.word_id = words.id 
            WHERE user_progress.user_id = ? AND user_progress.state = seen AND words.language = ? 
             AND user_progress.interval < 3600
            ORDER BY due LIMIT 1""", session["user_id"], session["language"])
        
        # if there are no cards left to review, display session over
        if not card:
            return render_template ("end_review.html")

        else:
            session["card"]= card[0]["words.id"]
            return render_template ("card.html", card = card)
        
            

@app.route("/search_decks" methods=["GET", "POST"])
