# mets-guessing

A website that is meant to somewhat resemble Wordle and WARdle (https://mlbpickle.com/) but with only New York Mets players.

The front-end UI is very bare with little style. The point of this project was not to make a pretty front-end, but instead to stitch together a funcitoning front-end while focusing on the back-end.

An API-like backend built using flask is what the website runs on. POST requests are sent to the backend for each guess, and a GET request is made with the necessary information regarding the guess which is run through a few async javascript functions that alter the table in the DOM to show the guess in the UI.

I may revisit this project later to add working user statistics, prettify the UI, or something else.

For now, it is deployed at https://mets-guessing.herokuapp.com/
