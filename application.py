import os
import selenium
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
from bs4 import BeautifulSoup
import requests
import pandas as pd

from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///diarycards.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
     raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    # get user's current module
    user_module = db.execute("SELECT module FROM users WHERE id = :user_id", user_id=session["user_id"])
    user_module = user_module[0]["module"]
    if user_module == 1:
        user_module = "Core Mindfulness"
    elif user_module == 2:
        user_module = "Emotion Regulation"
    elif user_module == 3:
        user_module = "Distress Tolerance"
    elif user_module == 4:
        user_module = "Interpersonal Effectiveness"
    else:
        user_module = "No module selected"
    # get average hours sleep
    avg_sleep = db.execute("SELECT AVG(sleep) FROM diarycards WHERE user_id = :user_id", user_id = session["user_id"])[0]["AVG(sleep)"]
    avg_sleep = round(avg_sleep)
    # get average si_urges
    avg_si_urges = db.execute("SELECT AVG(si_urges) FROM diarycards WHERE user_id = :user_id", user_id = session["user_id"])[0]["AVG(si_urges)"]
    avg_si_urges = round(avg_si_urges)
    # get average sh_urges
    avg_sh_urges = db.execute("SELECT AVG(sh_urges) FROM diarycards WHERE user_id = :user_id", user_id = session["user_id"])[0]["AVG(sh_urges)"]
    avg_sh_urges = round(avg_sh_urges)

    # get skills used in last 7 days
    wisemind = len(db.execute("SELECT wisemind FROM skills WHERE user_id = :user_id AND wisemind=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    observe = len(db.execute("SELECT observe FROM skills WHERE user_id = :user_id AND observe=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    describe = len(db.execute("SELECT describe FROM skills WHERE user_id = :user_id AND describe=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    participate = len(db.execute("SELECT participate FROM skills WHERE user_id = :user_id AND participate=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    nonjudgmental_stance = len(db.execute("SELECT nonjudgmental_stance FROM skills WHERE user_id = :user_id AND nonjudgmental_stance=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    one_mindfully = len(db.execute("SELECT one_mindfully FROM skills WHERE user_id = :user_id AND one_mindfully=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    effectiveness = len(db.execute("SELECT effectiveness FROM skills WHERE user_id = :user_id AND effectiveness = 1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))

    identified_emotion = len(db.execute("SELECT identified_emotion FROM skills WHERE user_id = :user_id AND identified_emotion=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    identified_emotion_function = len(db.execute("SELECT identified_emotion_function FROM skills WHERE user_id = :user_id AND identified_emotion_function = 1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    check_facts = len(db.execute("SELECT check_facts FROM skills WHERE user_id = :user_id AND check_facts=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    opposite_action = len(db.execute("SELECT opposite_action FROM skills WHERE user_id = :user_id AND opposite_action=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    problem_solving = len(db.execute("SELECT problem_solving FROM skills WHERE user_id = :user_id AND problem_solving=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    positives_short = len(db.execute("SELECT positives_short FROM skills WHERE user_id = :user_id AND positives_short=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    positives_long = len(db.execute("SELECT positives_long FROM skills WHERE user_id = :user_id AND positives_long=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    build_mastery = len(db.execute("SELECT build_mastery FROM skills WHERE user_id = :user_id AND build_mastery=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    cope_ahead = len(db.execute("SELECT cope_ahead FROM skills WHERE user_id = :user_id AND cope_ahead=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    reduce_vulnerability = len(db.execute("SELECT reduce_vulnerability FROM skills WHERE user_id = :user_id AND reduce_vulnerability=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    mindfulness_emotion = len(db.execute("SELECT mindfulness_emotion FROM skills WHERE user_id = :user_id AND mindfulness_emotion=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))

    stop_ = len(db.execute("SELECT stop_ FROM skills WHERE user_id = :user_id AND stop_=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    pros_cons = len(db.execute("SELECT pros_cons FROM skills WHERE user_id = :user_id AND pros_cons = 1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    tipp = len(db.execute("SELECT tipp FROM skills WHERE user_id = :user_id AND tipp=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    wm_accepts = len(db.execute("SELECT wm_accepts FROM skills WHERE user_id = :user_id AND wm_accepts=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    self_soothing = len(db.execute("SELECT self_soothing FROM skills WHERE user_id = :user_id AND self_soothing=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    improve = len(db.execute("SELECT improve FROM skills WHERE user_id = :user_id AND improve=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    radical_acceptance = len(db.execute("SELECT radical_acceptance FROM skills WHERE user_id = :user_id AND radical_acceptance=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    turning_mind = len(db.execute("SELECT turning_mind FROM skills WHERE user_id = :user_id AND turning_mind=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    willingness = len(db.execute("SELECT willingness FROM skills WHERE user_id = :user_id AND willingness=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    allowing_mind = len(db.execute("SELECT allowing_mind FROM skills WHERE user_id = :user_id AND allowing_mind=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))

    objective_effectiveness = len(db.execute("SELECT objective_effectiveness FROM skills WHERE user_id = :user_id AND objective_effectiveness=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    relationship_effectiveness = len(db.execute("SELECT relationship_effectiveness FROM skills WHERE user_id = :user_id AND relationship_effectiveness=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    selfrespect_effectiveness = len(db.execute("SELECT selfrespect_effectiveness FROM skills WHERE user_id = :user_id AND selfrespect_effectiveness=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))
    attending_relationships = len(db.execute("SELECT attending_relationships FROM skills WHERE user_id = :user_id AND attending_relationships=1 ORDER BY date DESC LIMIT 7", user_id = session["user_id"]))

    return render_template("index.html", attending_relationships=attending_relationships,selfrespect_effectiveness=selfrespect_effectiveness,relationship_effectiveness=relationship_effectiveness,objective_effectiveness=objective_effectiveness,allowing_mind=allowing_mind,willingness=willingness,turning_mind=turning_mind,radical_acceptance=radical_acceptance,improve=improve,self_soothing=self_soothing,wm_accepts=wm_accepts,tipp=tipp,pros_cons=pros_cons,stop_=stop_,mindfulness_emotion=mindfulness_emotion,reduce_vulnerability=reduce_vulnerability,cope_ahead=cope_ahead,build_mastery=build_mastery,positives_long=positives_long,positives_short = positives_short, problem_solving = problem_solving, opposite_action = opposite_action, check_facts = check_facts, effectiveness = effectiveness, identified_emotion = identified_emotion, identified_emotion_function = identified_emotion_function, user_module = user_module, wisemind = wisemind, observe = observe, describe = describe, one_mindfully = one_mindfully, participate = participate, nonjudgmental_stance = nonjudgmental_stance, avg_sleep = avg_sleep, avg_si_urges = avg_si_urges, avg_sh_urges = avg_sh_urges)

@app.route("/dashboard")
@login_required
def dashboard():
    user_module = db.execute("SELECT module FROM users WHERE id = :user_id", user_id=session["user_id"])
    user_module = user_module[0]["module"]
    if user_module == 1:
        user_module = "Core Mindfulness"
    elif user_module == 2:
        user_module = "Emotion Regulation"
    elif user_module == 3:
        user_module = "Distress Tolerance"
    elif user_module == 4:
        user_module = "Interpersonal Effectiveness"
    else:
        user_module = "No module selected"
    return render_template("index.html", user_module = user_module)

@app.route("/diarycard")
@login_required
def diarycard():
    rows = db.execute("SELECT date, si_urges, sh_urges, pain, sad, guilt, shame, anger, fear, happy, meds, sleep, skills_used FROM diarycards WHERE user_id = :user_id ORDER BY date DESC LIMIT 7", user_id = session["user_id"])
    for row in rows:
        date = row["date"]
        si_urges = row["si_urges"]
        sh_urges = row["sh_urges"]
        pain = row["pain"]
        sad = row["sad"]
        guilt = row["guilt"]
        shame = row["shame"]
        anger = row["anger"]
        fear = row["fear"]
        happy = row["happy"]
        sleep = row["sleep"]
        skills_used = row["skills_used"]
        if row["meds"] == 0:
            meds = "No"
        elif row["meds"] == 1:
            meds = "Yes"
    return render_template("diarycard.html", rows = rows, row = row, date = date, si_urges = si_urges, sh_urges = sh_urges, pain = pain, sad = sad, guilt = guilt, shame = shame, anger = anger, fear = fear, happy = happy, meds = meds, sleep = sleep, skills_used = skills_used)

@app.route("/diarycardhistory")
@login_required
def diarycardhistory():
    rows = db.execute("SELECT date, si_urges, sh_urges, pain, sad, guilt, shame, anger, fear, happy, meds, sleep, skills_used FROM diarycards WHERE user_id = :user_id ORDER BY date ASC", user_id = session["user_id"])
    for row in rows:
        date = row["date"]
        si_urges = row["si_urges"]
        sh_urges = row["sh_urges"]
        pain = row["pain"]
        sad = row["sad"]
        guilt = row["guilt"]
        shame = row["shame"]
        anger = row["anger"]
        fear = row["fear"]
        happy = row["happy"]
        sleep = row["sleep"]
        skills_used = row["skills_used"]
        if row["meds"] == 0:
            meds = "No"
        elif row["meds"] == 1:
            meds = "Yes"
    return render_template("diarycardhistory.html", rows = rows, row = row, date = date, si_urges = si_urges, sh_urges = sh_urges, pain = pain, sad = sad, guilt = guilt, shame = shame, anger = anger, fear = fear, happy = happy, meds = meds, sleep = sleep, skills_used = skills_used)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology")
        # Query database for username, returns a row with that username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/selectmodule", methods=["GET", "POST"])
@login_required
def selectmodule():
    """Select a module"""
    if request.method == "GET":
        return render_template("selectmodule.html")
    else:
        # get input from list and set to module
        module = int(request.form.get("module"))
        db.execute("UPDATE users SET module = :module WHERE id = :user_id", user_id = session["user_id"], module=module)
        flash(f"Successfully changed module")
        return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # If request method was GET
    if request.method == "GET":
        return render_template("signup.html")
    # If request method was POST
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # check if username exists
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)
        # check if password exists
        elif not password:
                return apology("invalid password", 403)
        # check if confirmation exists
        elif not confirmation:
                return apology("invalid password", 403)
        # check passwords match
        elif password != confirmation:
            return apology("passwords must match", 403)
        # check if username taken
        rows = db.execute("SELECT username FROM users WHERE username = :username", username=username)
        if (len(rows) != 0):
            return apology("username taken", 403)
        else:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8))
            if new_user:
                # Keep newly registered user logged in
                session["user_id"] = new_user
                # Flash info for the user
                flash(f"Registered as {username}")
                # Redirect user to homepage
                return redirect("/")

@app.route("/skills")
@login_required
def skills():

    # working code below
    rows = db.execute("SELECT * FROM skills WHERE user_id = :user_id ORDER BY date DESC LIMIT 7", user_id = session["user_id"])
    for row in rows:
        date = row["date"]
        wisemind = row["wisemind"]
        observe = row["observe"]
        describe = row["describe"]
        participate = row["participate"]
        nonjudgmental_stance = row["nonjudgmental_stance"]
        one_mindfully = row["one_mindfully"]
        effectiveness = row["effectiveness"]
        identified_emotion = row["identified_emotion"]
        identified_emotion_function = row["identified_emotion_function"]
        check_facts = row["check_facts"]
        opposite_action = row["opposite_action"]
        problem_solving = row["problem_solving"]
        positives_short = row["positives_short"]
        positives_long = row["positives_long"]
        build_mastery = row["build_mastery"]
        cope_ahead = row["cope_ahead"]
        reduce_vulnerability = row["reduce_vulnerability"]
        mindfulness_emotion = row["mindfulness_emotion"]
        stop_ = row["stop_"]
        pros_cons = row["pros_cons"]
        tipp = row["tipp"]
        wm_accepts = row["wm_accepts"]
        self_soothing = row["self_soothing"]
        improve = row["improve"]
        radical_acceptance = row["radical_acceptance"]
        turning_mind = row["turning_mind"]
        willingness = row["willingness"]
        allowing_mind = row["allowing_mind"]
        objective_effectiveness = row["objective_effectiveness"]
        relationship_effectiveness = row["relationship_effectiveness"]
        selfrespect_effectiveness = row["selfrespect_effectiveness"]
        attending_relationships = row["attending_relationships"]

        if row["wisemind"] == 1:
            row["wisemind"] = "Wise Mind"
        elif row["wisemind"] == 0:
            row["wisemind"] = ''

        if row["observe"] == 1:
            row["observe"] = "Observe"
        elif row["observe"] == 0:
            row["observe"] = ''

        if row["describe"] == 1:
            row["describe"] = "Describe"
        elif row["describe"] == 0:
            row["describe"] = ''

        if row["participate"] == 1:
            row["participate"] = "Participate"
        elif row["participate"] == 0:
            row["participate"] = ""

        if row["participate"] == 1:
            row["participate"] = "Participate"
        elif row["participate"] == 0:
            row["participate"] = ""

        if row["nonjudgmental_stance"] == 1:
            row["nonjudgmental_stance"] = "Nonjudgmental stance"
        elif row["nonjudgmental_stance"] == 0:
            row["nonjudgmental_stance"] = ''

        if row["one_mindfully"] == 1:
            row["one_mindfully"] = "One-mindfully"
        elif row["one_mindfully"] == 0:
            row["one_mindfully"] = ""
        if row["effectiveness"] == 1:
            row["effectiveness"] = "Effectiveness"
        elif row["effectiveness"] == 0:
            row["effectiveness"] = ""

        if row["identified_emotion"] == 1:
            row["identified_emotion"] = "Identified my emotion"
        elif row["identified_emotion"] == 0:
            row["identified_emotion"] = ''

        if row["identified_emotion_function"] == 1:
            row["identified_emotion_function"] = "Identified function of my emotion"
        elif row["identified_emotion_function"] == 0:
            row["identified_emotion_function"] = ''

        if row["check_facts"] == 1:
            row["check_facts"] = "Check the facts"
        elif row["check_facts"] == 0:
            row["check_facts"] = ''

        if row["opposite_action"] == 1:
            row["opposite_action"] = "Opposite action"
        elif row["opposite_action"] == 0:
            row["opposite_action"] = ''

        if row["problem_solving"] == 1:
            row["problem_solving"] = "Problem solving"
        elif row["problem_solving"] == 0:
            row["problem_solving"] = ''

        if row["positives_short"] == 1:
            row["positives_short"] = "Accumulate positives: short-term"
        elif row["positives_short"] == 0:
            row["positives_short"] = ''

        if row["positives_long"] == 1:
            row["positives_long"] = "Accumulate positives: long-term"
        elif row["positives_long"] == 0:
            row["positives_long"] = ''

        if row["build_mastery"] == 1:
            row["build_mastery"] = "Build mastery"
        elif row["build_mastery"] == 0:
            row["build_mastery"] = ''

        if row["cope_ahead"] == 1:
            row["cope_ahead"] = "Cope ahead"
        elif row["cope_ahead"] == 0:
            row["cope_ahead"] = ''
        if row["reduce_vulnerability"] == 1:
            row["reduce_vulnerability"] = "Reduce vulnerability"
        elif row["reduce_vulnerability"] == 0:
            row["reduce_vulnerability"] = ''
        if row["mindfulness_emotion"] == 1:
            row["mindfulness_emotion"] = "Mindfulness of current emotion"
        elif row["mindfulness_emotion"] == 0:
            row["mindfulness_emotion"] = ''

        if row["stop_"] == 1:
            row["stop_"] = "STOP"
        elif row["stop_"] == 0:
            row["stop_"] = ''

        if row["pros_cons"] == 1:
            row["pros_cons"] = "Pros and cons"
        elif row["pros_cons"] == 0:
            row["pros_cons"] = ''

        if row["tipp"] == 1:
            row["tipp"] = "TIPP"
        elif row["tipp"] == 0:
            row["tipp"] = ''
        if row["wm_accepts"] == 1:
            row["wm_accepts"] = "Wise Mind ACCEPTS"
        elif row["wm_accepts"] == 0:
            row["wm_accepts"] = ''
        if row["self_soothing"] == 1:
            row["self_soothing"] = "Self-soothing"
        elif row["self_soothing"] == 0:
            row["self_soothing"] = ''
        if row["improve"] == 1:
            row["improve"] = "Improve the moment"
        elif row["improve"] == 0:
            row["improve"] = ''
        if row["radical_acceptance"] == 1:
            row["radical_acceptance"] = "Radical Acceptance"
        elif row["radical_acceptance"] == 0:
            row["radical_acceptance"] = ''
        if row["turning_mind"] == 1:
            row["turning_mind"] = "Turning the mind"
        elif row["turning_mind"] == 0:
            row["turning_mind"] = ''
        if row["willingness"] == 1:
            row["willingness"] = "Willingness"
        elif row["willingness"] == 0:
            row["willingness"] = ''

        if row["allowing_mind"] == 1:
            row["allowing_mind"] = "Allowing the mind"
        elif row["allowing_mind"] == 0:
            row["allowing_mind"] = ''
        if row["objective_effectiveness"] == 1:
            row["objective_effectiveness"] = "Objective effectiveness"
        elif row["objective_effectiveness"] == 0:
            row["objective_effectiveness"] = ''
        if row["relationship_effectiveness"] == 1:
            row["relationship_effectiveness"] = "Relationship effectiveness"
        elif row["relationship_effectiveness"] == 0:
            row["relationship_effectiveness"] = ''
        if row["selfrespect_effectiveness"] == 1:
            row["selfrespect_effectiveness"] = "Self-respect effectiveness"
        elif row["selfrespect_effectiveness"] == 0:
            row["selfrespect_effectiveness"] = ''
        if row["attending_relationships"] == 1:
            row["attending_relationships"] = "Attending to relationships"
        elif row["attending_relationships"] == 0:
            row["attending_relationships"] = ''


    return render_template("skills.html", rows = rows, row = row, date = date, wisemind = wisemind, observe = observe, describe = describe, participate = participate, nonjudgmental_stance = nonjudgmental_stance, one_mindfully = one_mindfully, effectiveness = effectiveness, identified_emotion = identified_emotion, identified_emotion_function = identified_emotion_function, check_facts = check_facts,opposite_action = opposite_action, problem_solving = problem_solving, positives_short = positives_short, positives_long = positives_long, build_mastery = build_mastery, cope_ahead = cope_ahead, reduce_vulnerability = reduce_vulnerability, mindfulness_emotion = mindfulness_emotion, stop_ = stop_, pros_cons = pros_cons, tipp = tipp, wm_accepts = wm_accepts, self_soothing = self_soothing, improve = improve, radical_acceptance = radical_acceptance, turning_mind = turning_mind, willingness = willingness, allowing_mind = allowing_mind, objective_effectiveness = objective_effectiveness, relationship_effectiveness = relationship_effectiveness, selfrespect_effectiveness = selfrespect_effectiveness, attending_relationships = attending_relationships)


@app.route("/skillshistory")
@login_required
def skillshistory():
    # find sum of each skills used
    wisemind_count = db.execute("SELECT SUM(wisemind) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(wisemind)"]
    observe_count = db.execute("SELECT SUM(observe) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(observe)"]
    describe_count = db.execute("SELECT SUM(describe) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(describe)"]
    participate_count = db.execute("SELECT SUM(participate) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(participate)"]
    nonjudgmental_stance_count = db.execute("SELECT SUM(nonjudgmental_stance) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(nonjudgmental_stance)"]
    one_mindfully_count = db.execute("SELECT SUM(one_mindfully) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(one_mindfully)"]
    effectiveness_count = db.execute("SELECT SUM(effectiveness) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(effectiveness)"]

    identified_emotion_count = db.execute("SELECT SUM(identified_emotion) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(identified_emotion)"]
    identified_emotion_function_count = db.execute("SELECT SUM(identified_emotion_function) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(identified_emotion_function)"]
    check_facts_count = db.execute("SELECT SUM(check_facts) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(check_facts)"]
    opposite_action_count = db.execute("SELECT SUM(opposite_action) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(opposite_action)"]
    problem_solving_count = db.execute("SELECT SUM(problem_solving) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(problem_solving)"]
    positives_short_count = db.execute("SELECT SUM(positives_short) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(positives_short)"]
    positives_long_count = db.execute("SELECT SUM(positives_long) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(positives_long)"]
    build_mastery_count = db.execute("SELECT SUM(build_mastery) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(build_mastery)"]
    cope_ahead_count = db.execute("SELECT SUM(cope_ahead) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(cope_ahead)"]
    reduce_vulnerability_count = db.execute("SELECT SUM(reduce_vulnerability) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(reduce_vulnerability)"]
    mindfulness_emotion_count = db.execute("SELECT SUM(mindfulness_emotion) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(mindfulness_emotion)"]

    stop_count = db.execute("SELECT SUM(stop_) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(stop_)"]
    pros_cons_count = db.execute("SELECT SUM(pros_cons) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(pros_cons)"]
    tipp_count = db.execute("SELECT SUM(tipp) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(tipp)"]
    wm_accepts_count = db.execute("SELECT SUM(wm_accepts) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(wm_accepts)"]
    self_soothing_count = db.execute("SELECT SUM(self_soothing) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(self_soothing)"]
    improve_count = db.execute("SELECT SUM(improve) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(improve)"]
    radical_acceptance_count = db.execute("SELECT SUM(radical_acceptance) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(radical_acceptance)"]
    turning_mind_count = db.execute("SELECT SUM(turning_mind) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(turning_mind)"]
    willingness_count = db.execute("SELECT SUM(willingness) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(willingness)"]
    allowing_mind_count = db.execute("SELECT SUM(allowing_mind) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(allowing_mind)"]

    objective_effectiveness_count = db.execute("SELECT SUM(objective_effectiveness) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(objective_effectiveness)"]
    relationship_effectiveness_count = db.execute("SELECT SUM(relationship_effectiveness) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(relationship_effectiveness)"]
    selfrespect_effectiveness_count = db.execute("SELECT SUM(selfrespect_effectiveness) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(selfrespect_effectiveness)"]
    attending_relationships_count = db.execute("SELECT SUM(attending_relationships) FROM skills WHERE user_id = :user_id", user_id = session["user_id"])[0]["SUM(attending_relationships)"]

    # put skills counts in a list
    counts = [wisemind_count,observe_count,describe_count,participate_count,nonjudgmental_stance_count,one_mindfully_count,effectiveness_count,identified_emotion_count,identified_emotion_function_count,check_facts_count,opposite_action_count,problem_solving_count,positives_short_count,positives_long_count,build_mastery_count,cope_ahead_count,reduce_vulnerability_count,mindfulness_emotion_count,stop_count,pros_cons_count,tipp_count,wm_accepts_count,self_soothing_count,improve_count,radical_acceptance_count,turning_mind_count,willingness_count,allowing_mind_count,objective_effectiveness_count,relationship_effectiveness_count,selfrespect_effectiveness_count,attending_relationships_count]

    # execute table
    rows = db.execute("SELECT * FROM skills WHERE user_id = :user_id ORDER BY date DESC LIMIT 7", user_id = session["user_id"])
    for row in rows:
        date = row["date"]
        wisemind = row["wisemind"]
        observe = row["observe"]
        describe = row["describe"]
        participate = row["participate"]
        nonjudgmental_stance = row["nonjudgmental_stance"]
        one_mindfully = row["one_mindfully"]
        effectiveness = row["effectiveness"]
        identified_emotion = row["identified_emotion"]
        identified_emotion_function = row["identified_emotion_function"]
        check_facts = row["check_facts"]
        opposite_action = row["opposite_action"]
        problem_solving = row["problem_solving"]
        positives_short = row["positives_short"]
        positives_long = row["positives_long"]
        build_mastery = row["build_mastery"]
        cope_ahead = row["cope_ahead"]
        reduce_vulnerability = row["reduce_vulnerability"]
        mindfulness_emotion = row["mindfulness_emotion"]
        stop_ = row["stop_"]
        pros_cons = row["pros_cons"]
        tipp = row["tipp"]
        wm_accepts = row["wm_accepts"]
        self_soothing = row["self_soothing"]
        improve = row["improve"]
        radical_acceptance = row["radical_acceptance"]
        turning_mind = row["turning_mind"]
        willingness = row["willingness"]
        allowing_mind = row["allowing_mind"]
        objective_effectiveness = row["objective_effectiveness"]
        relationship_effectiveness = row["relationship_effectiveness"]
        selfrespect_effectiveness = row["selfrespect_effectiveness"]
        attending_relationships = row["attending_relationships"]

        if row["wisemind"] == 1:
            row["wisemind"] = "Wise Mind"
        elif row["wisemind"] == 0:
            row["wisemind"] = ''

        if row["observe"] == 1:
            row["observe"] = "Observe"
        elif row["observe"] == 0:
            row["observe"] = ''

        if row["describe"] == 1:
            row["describe"] = "Describe"
        elif row["describe"] == 0:
            row["describe"] = ''

        if row["participate"] == 1:
            row["participate"] = "Participate"
        elif row["participate"] == 0:
            row["participate"] = ""

        if row["participate"] == 1:
            row["participate"] = "Participate"
        elif row["participate"] == 0:
            row["participate"] = ""

        if row["nonjudgmental_stance"] == 1:
            row["nonjudgmental_stance"] = "Nonjudgmental stance"
        elif row["nonjudgmental_stance"] == 0:
            row["nonjudgmental_stance"] = ''

        if row["one_mindfully"] == 1:
            row["one_mindfully"] = "One-mindfully"
        elif row["one_mindfully"] == 0:
            row["one_mindfully"] = ""
        if row["effectiveness"] == 1:
            row["effectiveness"] = "Effectiveness"
        elif row["effectiveness"] == 0:
            row["effectiveness"] = ""

        if row["identified_emotion"] == 1:
            row["identified_emotion"] = "Identified my emotion"
        elif row["identified_emotion"] == 0:
            row["identified_emotion"] = ''

        if row["identified_emotion_function"] == 1:
            row["identified_emotion_function"] = "Identified function of my emotion"
        elif row["identified_emotion_function"] == 0:
            row["identified_emotion_function"] = ''

        if row["check_facts"] == 1:
            row["check_facts"] = "Check the facts"
        elif row["check_facts"] == 0:
            row["check_facts"] = ''

        if row["opposite_action"] == 1:
            row["opposite_action"] = "Opposite action"
        elif row["opposite_action"] == 0:
            row["opposite_action"] = ''

        if row["problem_solving"] == 1:
            row["problem_solving"] = "Problem solving"
        elif row["problem_solving"] == 0:
            row["problem_solving"] = ''

        if row["positives_short"] == 1:
            row["positives_short"] = "Accumulate positives: short-term"
        elif row["positives_short"] == 0:
            row["positives_short"] = ''

        if row["positives_long"] == 1:
            row["positives_long"] = "Accumulate positives: long-term"
        elif row["positives_long"] == 0:
            row["positives_long"] = ''

        if row["build_mastery"] == 1:
            row["build_mastery"] = "Build mastery"
        elif row["build_mastery"] == 0:
            row["build_mastery"] = ''

        if row["cope_ahead"] == 1:
            row["cope_ahead"] = "Cope ahead"
        elif row["cope_ahead"] == 0:
            row["cope_ahead"] = ''
        if row["reduce_vulnerability"] == 1:
            row["reduce_vulnerability"] = "Reduce vulnerability"
        elif row["reduce_vulnerability"] == 0:
            row["reduce_vulnerability"] = ''
        if row["mindfulness_emotion"] == 1:
            row["mindfulness_emotion"] = "Mindfulness of current emotion"
        elif row["mindfulness_emotion"] == 0:
            row["mindfulness_emotion"] = ''

        if row["stop_"] == 1:
            row["stop_"] = "STOP"
        elif row["stop_"] == 0:
            row["stop_"] = ''

        if row["pros_cons"] == 1:
            row["pros_cons"] = "Pros and cons"
        elif row["pros_cons"] == 0:
            row["pros_cons"] = ''

        if row["tipp"] == 1:
            row["tipp"] = "TIPP"
        elif row["tipp"] == 0:
            row["tipp"] = ''
        if row["wm_accepts"] == 1:
            row["wm_accepts"] = "Wise Mind ACCEPTS"
        elif row["wm_accepts"] == 0:
            row["wm_accepts"] = ''
        if row["self_soothing"] == 1:
            row["self_soothing"] = "Self-soothing"
        elif row["self_soothing"] == 0:
            row["self_soothing"] = ''
        if row["improve"] == 1:
            row["improve"] = "Improve the moment"
        elif row["improve"] == 0:
            row["improve"] = ''
        if row["radical_acceptance"] == 1:
            row["radical_acceptance"] = "Radical Acceptance"
        elif row["radical_acceptance"] == 0:
            row["radical_acceptance"] = ''
        if row["turning_mind"] == 1:
            row["turning_mind"] = "Turning the mind"
        elif row["turning_mind"] == 0:
            row["turning_mind"] = ''
        if row["willingness"] == 1:
            row["willingness"] = "Willingness"
        elif row["willingness"] == 0:
            row["willingness"] = ''

        if row["allowing_mind"] == 1:
            row["allowing_mind"] = "Allowing the mind"
        elif row["allowing_mind"] == 0:
            row["allowing_mind"] = ''
        if row["objective_effectiveness"] == 1:
            row["objective_effectiveness"] = "Objective effectiveness"
        elif row["objective_effectiveness"] == 0:
            row["objective_effectiveness"] = ''
        if row["relationship_effectiveness"] == 1:
            row["relationship_effectiveness"] = "Relationship effectiveness"
        elif row["relationship_effectiveness"] == 0:
            row["relationship_effectiveness"] = ''
        if row["selfrespect_effectiveness"] == 1:
            row["selfrespect_effectiveness"] = "Self-respect effectiveness"
        elif row["selfrespect_effectiveness"] == 0:
            row["selfrespect_effectiveness"] = ''
        if row["attending_relationships"] == 1:
            row["attending_relationships"] = "Attending to relationships"
        elif row["attending_relationships"] == 0:
            row["attending_relationships"] = ''

    return render_template("skillshistory.html", counts = counts, rows = rows, row = row, date = date, wisemind = wisemind, observe = observe, describe = describe, participate = participate, nonjudgmental_stance = nonjudgmental_stance, one_mindfully = one_mindfully, effectiveness = effectiveness, identified_emotion = identified_emotion, identified_emotion_function = identified_emotion_function, check_facts = check_facts,opposite_action = opposite_action, problem_solving = problem_solving, positives_short = positives_short, positives_long = positives_long, build_mastery = build_mastery, cope_ahead = cope_ahead, reduce_vulnerability = reduce_vulnerability, mindfulness_emotion = mindfulness_emotion, stop_ = stop_, pros_cons = pros_cons, tipp = tipp, wm_accepts = wm_accepts, self_soothing = self_soothing, improve = improve, radical_acceptance = radical_acceptance, turning_mind = turning_mind, willingness = willingness, allowing_mind = allowing_mind, objective_effectiveness = objective_effectiveness, relationship_effectiveness = relationship_effectiveness, selfrespect_effectiveness = selfrespect_effectiveness, attending_relationships = attending_relationships)


@app.route("/tips", methods=["GET", "POST"])
@login_required
def tips():
    """Display  Tips & Tricks"""
    if request.method == "GET":
        tips = db.execute("SELECT tip FROM tips WHERE user_id = :user_id", user_id=session["user_id"])
        print(tips[0]['tip'])
        user_module = db.execute("SELECT module FROM users WHERE id = :user_id", user_id=session["user_id"])[0]['module']
        if user_module == 1:
            user_module = "Core Mindfulness"
        elif user_module == 2:
            user_module = "Emotion Regulation"
        elif user_module == 3:
            user_module = "Distress Tolerance"
        elif user_module == 4:
            user_module = "Core Mindfulness"
        mtips = db.execute("SELECT tip FROM tips WHERE user_id = :user_id AND module = 'Emotion Regulation'", user_id=session["user_id"])
        return render_template("tips.html", tips = tips, user_module = user_module, mtips=mtips)
    else:
        try:
            # get input from user
            tip = request.form.get("tiptextarea")
            module = request.form.get("moduledropdown")
            today = date.today()
            # insert into tips db
            db.execute("INSERT INTO tips (user_id, date, tip, module) VALUES (:user_id, :date, :tip, :module)", user_id = session["user_id"],
            date = today, tip = tip, module = module)
            # redirect
            flash("Added your custom tip")
            return redirect("/tips")
        except:
            # Flash info for the user
            flash(f"Failed to add tip: please complete all fields")
            # return to index
            return render_template("tips.html", tips = tips)

@app.route("/cmtips")
@login_required
def cmtips():
    """Display cm Tips """
    mtips = db.execute("SELECT tip FROM tips WHERE user_id = :user_id AND module = 'Core Mindfulness'", user_id=session["user_id"])
    return render_template("cmtips.html", mtips = mtips)

@app.route("/ertips")
@login_required
def ertips():
    """Display er Tips """
    mtips = db.execute("SELECT tip FROM tips WHERE user_id = :user_id AND module = 'Emotion Regulation'", user_id=session["user_id"])
    return render_template("ertips.html", mtips = mtips)

@app.route("/dttips")
@login_required
def dttips():
    """Display dt Tips """
    mtips = db.execute("SELECT tip FROM tips WHERE user_id = :user_id AND module = 'Distress Tolerance'", user_id=session["user_id"])
    return render_template("dttips.html", mtips = mtips)

@app.route("/ietips")
@login_required
def ietips():
    """Display ie Tips """
    mtips = db.execute("SELECT tip FROM tips WHERE user_id = :user_id AND module = 'Interpersonal Effectiveness'", user_id=session["user_id"])
    return render_template("ietips.html", mtips = mtips)

@app.route("/updatecard", methods=["GET", "POST"])
@login_required
def updatecard():
    if request.method == "GET":
        return render_template("updatecard.html")
    else:
        try:
            # set form inputs to variables
            date = request.form.get("date_input")
            si_urges = int(request.form.get("si_urges"))
            sh_urges = int(request.form.get("sh_urges"))
            pain = int(request.form.get("pain"))
            sad = int(request.form.get("sad"))
            guilt = int(request.form.get("guilt"))
            shame = int(request.form.get("shame"))
            anger = int(request.form.get("anger"))
            fear = int(request.form.get("fear"))
            happy = int(request.form.get("happy"))
            meds = bool(request.form.get("meds"))
            sleep = int(request.form.get("sleep"))
            skills_used = int(request.form.get("skills_used"))
        except TypeError:
            # Flash info for the user
            flash(f"Failed to update diary card: please complete all fields")
            # return to index
            return render_template("updatecard.html")
        # insert new variables into diarycards table
        try:
            db.execute("INSERT INTO diarycards (user_id, date, si_urges, sh_urges, pain, sad, guilt, shame, anger, fear, happy, meds, sleep, skills_used) VALUES (:user_id, :date, :si_urges, :sh_urges, :pain, :sad, :guilt, :shame, :anger, :fear, :happy, :meds, :sleep, :skills_used)",
                        user_id = session["user_id"],
                        date = date,
                        si_urges = si_urges,
                        sh_urges = sh_urges,
                        pain = pain,
                        sad = sad,
                        guilt = guilt,
                        shame = shame,
                        anger = anger,
                        fear = fear,
                        happy = happy,
                        meds = meds,
                        sleep = sleep,
                        skills_used = skills_used)
            # Flash info for the user
            flash(f"Updated diary card successfully.")
            # return to index
            return redirect("/")
        except TypeError:
            # Flash info for the user
            flash(f"Failed to update diary card: please complete all fields")
            # return to index
            return render_template("updatecard.html")

@app.route("/updateskills", methods=["GET", "POST"])
@login_required
def updateskills():
    if request.method == "GET":
        return render_template("updateskills.html")
    else:
        try:
            # set form inputs to variables
            date = request.form.get("date")
            wisemind = bool(request.form.get("wisemind"))
            observe = bool(request.form.get("observe"))
            describe = bool(request.form.get("describe"))
            participate = bool(request.form.get("participate"))
            nonjudgmental_stance = bool(request.form.get("nonjudgmental_stance"))
            one_mindfully = bool(request.form.get("one_mindfully"))
            effectiveness = bool(request.form.get("effectiveness"))
            identified_emotion = bool(request.form.get("identified_emotion"))
            identified_emotion_function = bool(request.form.get("identified_emotion_function"))
            check_facts = bool(request.form.get("check_facts"))
            opposite_action = bool(request.form.get("opposite_action"))
            problem_solving = bool(request.form.get("problem_solving"))
            positives_short = bool(request.form.get("positives_short"))
            positives_long = bool(request.form.get("positives_long"))
            build_mastery = bool(request.form.get("build_mastery"))
            cope_ahead = bool(request.form.get("cope_ahead"))
            reduce_vulnerability = bool(request.form.get("reduce_vulnerability"))
            mindfulness_emotion = bool(request.form.get("mindfulness_emotion"))
            stop_ = bool(request.form.get("stop_"))
            pros_cons = bool(request.form.get("pros_cons"))
            tipp = bool(request.form.get("tipp"))
            wm_accepts = bool(request.form.get("wm_accepts"))
            self_soothing = bool(request.form.get("self_soothing"))
            improve = bool(request.form.get("improve"))
            radical_acceptance = bool(request.form.get("radical_acceptance"))
            turning_mind = bool(request.form.get("turning_mind"))
            willingness = bool(request.form.get("willingness"))
            allowing_mind = bool(request.form.get("allowing_mind"))
            objective_effectiveness = bool(request.form.get("objective_effectiveness"))
            relationship_effectiveness = bool(request.form.get("relationship_effectiveness"))
            selfrespect_effectiveness = bool(request.form.get("selfrespect_effectiveness"))
            attending_relationships = bool(request.form.get("attending_relationships"))
        except:
            # Flash info for the user
            flash(f"Failed to update DBT Skills")
            # return to index
            return render_template("updateskills.html")
        try:
            # insert new variables into skills table
            db.execute("INSERT INTO skills (user_id, date, wisemind, observe, describe, participate, nonjudgmental_stance, one_mindfully, effectiveness, identified_emotion, identified_emotion_function, check_facts, opposite_action, problem_solving, positives_short, positives_long, build_mastery, cope_ahead, reduce_vulnerability, mindfulness_emotion, stop_, pros_cons, tipp, wm_accepts, self_soothing, improve, radical_acceptance, turning_mind, willingness, allowing_mind, objective_effectiveness, relationship_effectiveness, selfrespect_effectiveness, attending_relationships) VALUES (:user_id, :date, :wisemind, :observe, :describe, :participate, :nonjudgmental_stance, :one_mindfully, :effectiveness, :identified_emotion, :identified_emotion_function, :check_facts, :opposite_action, :problem_solving, :positives_short, :positives_long, :build_mastery, :cope_ahead, :reduce_vulnerability, :mindfulness_emotion, :stop_, :pros_cons, :tipp, :wm_accepts, :self_soothing, :improve, :radical_acceptance, :turning_mind, :willingness, :allowing_mind, :objective_effectiveness, :relationship_effectiveness, :selfrespect_effectiveness, :attending_relationships)",
                        user_id = session["user_id"],
                        date = date,
                        wisemind = wisemind,
                        observe = observe,
                        describe = describe,
                        participate = participate,
                        nonjudgmental_stance = nonjudgmental_stance,
                        one_mindfully = one_mindfully,
                        effectiveness = effectiveness,
                        identified_emotion = identified_emotion,
                        identified_emotion_function = identified_emotion_function,
                        check_facts = check_facts,
                        opposite_action = opposite_action,
                        problem_solving = problem_solving,
                        positives_short = positives_short,
                        positives_long = positives_long,
                        build_mastery = build_mastery,
                        cope_ahead = cope_ahead,
                        reduce_vulnerability = reduce_vulnerability,
                        mindfulness_emotion = mindfulness_emotion,
                        stop_ = stop_,
                        pros_cons = pros_cons,
                        tipp = tipp,
                        wm_accepts = wm_accepts,
                        self_soothing = self_soothing,
                        improve = improve,
                        radical_acceptance = radical_acceptance,
                        turning_mind = turning_mind,
                        willingness = willingness,
                        allowing_mind = allowing_mind,
                        objective_effectiveness = objective_effectiveness,
                        relationship_effectiveness = relationship_effectiveness,
                        selfrespect_effectiveness = selfrespect_effectiveness,
                        attending_relationships = attending_relationships)
            # Flash info for the user
            flash(f"Updated your DBT Skills successfully.")
            # return to index
            return redirect("/")
        except:
            # Flash info for the user
            flash(f"Failed to update DBT Skills")
            # return to index
            return render_template("updateskills.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)