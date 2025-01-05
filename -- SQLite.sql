-- SQLite
CREATE TABLE users (
id INT AUTO INCREMENT, 
username TEXT, 
hash TEXT
); 
CREATE TABLE words (
id INT AUTO INCREMENT, 
language TEXT, 
word TEXT, 
definition TEXT, 
frequency TEXT, 
example TEXT, 
part TEXT
);
CREATE TABLE user_progress (
user_id INT, 
word_id INT, 
interval INT, 
date INT, 
viewings INT, 
easy INT, 
good INT, 
ok INT, 
some INT, 
none INT, 
state TEXT
);
CREATE TABLE decks (
id INT AUTO INCREMENT, 
language TEXT, 
name TEXT, 
type TEXT, 
genre TEXT, 
author TEXT, 
date TEXT
);
CREATE TABLE deck_contents (
deck_id INT, 
card_id INT
);
CREATE TABLE users_to_decks (
user_id INT, 
deck_id INT
);
AMEND TABLE decks 
ADD size INTEGER;
AMEND TABLE users_to_decks
ADD progress FLOAT;
AMEND TABLE deck_contents
ADD frequency INT;
AMEND TABLE words
ADD common TEXT;