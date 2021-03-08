from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def index():
    return render_template("choose_survey.html", surveys=surveys.keys())


@app.route('/begin', methods=["POST"])
def begin():
    session["survey"] = request.form['survey']
    session["responses"] = []
    title = surveys[session["survey"]].title
    instructions = surveys[session["survey"]].instructions
    return render_template("survey_start.html", title=title, instructions=instructions)


@app.route('/questions/<int:index>')
def questions(index):
    if index != len(session["responses"]):
        flash('Nice try bro!')
        return redirect(f'/questions/{len(session["responses"])}')

    if index == len(surveys[session["survey"]].questions):
        return redirect('/thankyou')

    question = surveys[session["survey"]].questions[index]

    return render_template(
        "question.html",
        question=question
    )


@app.route('/answer', methods=["POST"])
def answer():
    responses = session["responses"]
    if request.form.get("comment"):
        responses.append((request.form["answer"], request.form["comment"]))
    else:
        responses.append((request.form["answer"],))
    session["responses"] = responses
    print(session["responses"])
    index = len(responses)
    return redirect(f"/questions/{index}")


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
