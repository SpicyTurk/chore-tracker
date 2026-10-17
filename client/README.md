#Chore Tracker
This is a full-stack web application that gives roommates a shared, permanent record of chores that each household member has done and when. 

#The Problem
Young adults who are transitioning into shared living often rely on chores being tracked on a whiteboard or in a group text. Whiteboards get erased and texts get buried, so nobody can look back and see who did what. That leads to arguments about whose turn it is and who has done the most.

Chore Tracker replaces both with a shared history. One roommate assigns a chore with a due date, and the person it was assigned to logs the exact date and time they finished it.

#Technologies used

Backend:

Python 3.8
    Flask
    Flask-SQLAlchemy (SQLAlchemy) with SQLite
    Flask-Migrate (database migrations)
    Flask-Bcrypt (password hashing)
    Flask-CORS

Frontend:
    React
    Vite
    ESLint

Tools:
    Git and GitHub
    curl, for testing the API
    VSCode 

#Running it on your system

You'll need Python 3.8 or newer, Node.js 18 or newer, and Git. I built this in VSCode, so the commands below are for a Unix-style terminal (macOS, Linux, or WSL on Windows).

1. Clone the repo
    bash
    git clone https://github.com/SpicyTurk/chore-tracker.git
    cd chore-tracker

2. Start the backend
    bash
    cd server
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=app.py
    flask db upgrade
    python3 app.py

The API will be running at http://localhost:5555. The flask db upgrade step creates an empty SQLite database (server/instance/chores.db) from the migration files.

Flask uses a secret key to sign login cookies. The app has a development key built in, but if you'd like to use your own, run export SECRET_KEY="whatever-you-like" before you start the server.

3. Start the frontend

Open a second terminal and run:
    bash
    cd client
    npm install
    npm run dev

The app will be at http://localhost:5173.

4. Try it out

Chores are passed between people, so you'll need two accounts to see the whole thing. Sign up as one user, log out, then sign up as a second user. Log back in as the first one and add a chore assigned to the second user's username. Then log in as the second user and log that the chore is done.

#What it does

Accounts:
    Sign up, log in, and log out
    Passwords are hashed with bcrypt, so the plain text is never stored or sent back
    Your login is kept in a session cookie, so refreshing the page doesn't log you out

Chores:
    Create a chore with a title, a due date, and the username of the person it's assigned to
    See a paginated list of the chores you created or were assigned, sorted by due date
    The person who created a chore can edit the title or due date, or delete it, as long as it hasn't been completed yet

Completions:
    Only the person a chore is assigned to can log it as done, with the date and time
    A chore can only be completed once, and the completion time can't be in the future
    The assignee can fix the time or delete their own log. Deleting it reopens the chore

Status:
    Every chore is pending, overdue (not done and past its due date), or completed
    Overdue chores get a red label in the list
    Chores that aren't done show their due date, and finished ones show when they were completed

Rules:
    -You can only see and change your own records
    -If something goes wrong, the API sends back a JSON message and a clear status code: 400 for bad input, 401 if you're not logged in, 403 if you're not allowed, 404 if it doesn't exist, and 409 if the chore's current state doesn't allow the change
    -The React app shows those messages next to the form that caused them

#How the data fits together

User: id, username (unique), password_hash

Chore: id, title, due_date, created_at, plus creator_id and assignee_id, which both point to a User

Complete (the completed table): id, chore_id (unique, so each chore can only have one completion), and completed_on, which holds the date and time

A user can create many chores and be assigned many chores. Each chore has one creator, one assignee, and at most one completion.

#API routes

Method	                Route	                            What it does
POST	                /signup	                            Create an account and log in
POST	                /login	                            Log in
DELETE	                /logout	                            Log out
GET	                    /check_session	                    Return the logged-in user, or 401
GET	                    /chores?page=1&per_page=10	        List your chores, one page at a time
POST	                /chores	                            Create a chore
PATCH	                /chores/<id>	                    Edit a chore (creator only, before it's completed)
DELETE	                /chores/<id>	                    Delete a chore (creator only, before it's completed)
POST	                /chores/<id>                        /completion	Log a completion (assignee only)
PATCH	                /chores/<id>                        /completion	Change a completion time (assignee only)
DELETE	                /chores/<id>                        /completion	Delete a completion log (assignee only)

per_page defaults to 10. If you ask for a page past the end, you get an empty list.

#Request bodies

Create a chore:
    { "title": "Wash dishes", "due": "2026-10-20", "assignee": "ben" }

Edit a chore (send one field or both):
    { "title": "Scrub the sink", "due_date": "2026-10-25" }

Log or edit a completion:
    { "completed_on": "2026-10-16T18:30" }

#What's not done yet

    -The interface covers signing up, logging in and out, creating chores, the paginated list, and logging completions. Editing and deleting chores, and editing or deleting a completion, work through the API (I tested them with curl) but don't have buttons in the interface yet.
    -It only runs locally. I haven't deployed it.
    -The list shows the chores you created or were assigned, not everything your roommates have done.

#Where I'd take it next

    -Edit and delete buttons in the interface
    -Past, current, and future views with time windows (week, month, 3 months, 6 months, year)
    -Monthly totals so roommates can see who has done what
    -Comments on chores, so people can talk through changes
    -Reminders for upcoming due dates
    -Deploying it

#If something goes wrong

    -ModuleNotFoundError: No module named 'flask_sqlalchemy': 
        your virtual environment isn't active. From the server folder, run source venv/bin/activate.

    -You get logged out or see 401 errors right after logging in: 
        check that the backend is running on port 5555 and the frontend on 5173. If Vite picked a different port, update the allowed origin in server/config.py to match.
        
    -A new terminal forgot FLASK_APP: 
        run export FLASK_APP=app.py again.