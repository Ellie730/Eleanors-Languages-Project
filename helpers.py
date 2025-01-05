import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

def presence(variable, vname):
    if not variable:
        return apology(f"please enter a {vname}")

languages = ["italian", "spanish"]

def update()
        #if new day reset new card counter
    last = db.execute ("SELECT time FROM users WHERE id = ?", session["user_id"])[0]["date"]
    if date.fromtimestamp(last) != date.today():
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
    
    




