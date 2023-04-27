import os
from spotify_api import (
    get_token,
    search_for_artist,
    get_songs_by_artist,
    get_related_artists,
    get_albums_by_artist
)
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from helpers import login_required
from dotenv import load_dotenv


# Configure application
app = Flask(__name__)

# Configure secret key
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
app.secret_key = SECRET_KEY

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure Sqlite3


def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
@login_required
def index():
    # Get current user
    username = session["username"]

    if username == '':
        return render_template("login.html")

    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":

        artist_name = ''

        # Ensure artist was submitted
        if not request.form.get("artist"):
            flash("Please enter an artist.")
            return render_template("index.html")

        try:
            # get an access token
            token = get_token()

            # artist to search for
            artist_name = request.form.get("artist")

            # search for an artist and retrieve their top songs
            artist_search_result = search_for_artist(token, artist_name)
            if artist_search_result is not None:
                artist_id = artist_search_result["id"]
                songs = get_songs_by_artist(token, artist_id)[:11]
                albums = get_albums_by_artist(token, artist_id)[:11]

                # search for similar artist and display them
                similar_artists_search_result = get_related_artists(
                    token, artist_id)
                if similar_artists_search_result is not None:
                    similar_artists = similar_artists_search_result[:5]

        except (KeyError, TypeError, ValueError):
            flash("KeyError, TypeError, ValueError")
            return render_template("index.html")

        return render_template("/search.html", songs=songs, similar_artists=similar_artists, enumerate=enumerate, artist_name=artist_name, albums=albums)

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter a username")
            return render_template("auth/register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please enter a password")
            return render_template("auth/register.html")

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            flash("Please confirm password")
            return render_template("auth/register.html")

        # Ensure password equal to confirm password
        if (request.form.get("password") != request.form.get("confirmation")):
            flash("Check if passwords match")
            return render_template("auth/register.html")

        # Insert username and password into database
        hash = generate_password_hash(request.form.get("password"))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                (request.form.get("username"), hash)
            )

            conn.commit()

            new_user = cursor.lastrowid

            cursor.close()
            conn.close()

            # Remember which user has logged in
            session["username"] = new_user

            return redirect("/")

        except:
            flash("User already registered, please login")
            return render_template("auth/login.html")

    return render_template("auth/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any username
    session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter a username")
            return render_template("auth/login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Please enter a password")
            return render_template("auth/login.html")

        # Query database for username
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM users WHERE username = ?",
                            (request.form.get("username"),)).fetchall()
        conn.close()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Incorrect username / password")
            return render_template("auth/login.html")

        # Remember which user has logged in
        session["username"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any username
    session.clear()

    # Redirect user to login form
    return redirect("/")
