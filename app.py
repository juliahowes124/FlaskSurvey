from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


"""
TODO:
-pre-fill form with previous answer, if any
-thank you page, show question with strikethrough if skipped
-clean up code
-styling
"We don’t want users to submit a survey more than once.
Of course, you could put something in the session that says they’ve completed that
survey, and check for that, but the cookies that support the session typically only
last as long as the browser is running — a user who quits their browser could re-answer
the survey. Figure out a way you could prevent a site visitor from re-filling-out
a survey using cookies."

"""
@app.route('/')
def index():
    return render_template("choose_survey.html", surveys=surveys.keys())


@app.route('/begin', methods=["POST"])
def begin():
    session["survey"] = request.form['survey']
    session["responses"] = [{"question": question.question} for question in surveys[session["survey"]].questions]
    session["current_index"] = 0
    session["in_survey"] = True
    title = surveys[session["survey"]].title
    instructions = surveys[session["survey"]].instructions
    return render_template("survey_start.html", title=title, instructions=instructions)


@app.route('/questions/<int:index>')
def questions(index):
    if not session["in_survey"]:
        flash("The survey is over")
        return redirect('/thankyou')

    questions = surveys[session["survey"]].questions
    if index > len(questions)-1:
        flash('Nice try')
        return redirect(f'/questions/{session["current_index"]}')

    return render_template(
        "question.html",
        question=questions[index],
        display_back=index > 0,
        display_next=index < len(questions)-1,
        display_finish=index == len(questions)-1
    )


@app.route('/answer', methods=["POST"])
def answer():
    responses = session["responses"]
    index = session["current_index"]
    questions = surveys[session["survey"]].questions
    question = questions[index].question
    responses[index] = {
        "question": question,
        "answer": request.form.get("answer"),
        "comment": request.form.get("comment")
    }
    session["responses"] = responses
    if session["current_index"] == len(questions)-1:
        return redirect('/thankyou')
    return redirect("/next")


@app.route('/thankyou')
def thankyou():
    responses = session["responses"]
    session["in_survey"] = False
    return render_template('thankyou.html', responses=responses)


@app.route('/back')
def go_back():
    index = session["current_index"]
    if not session["in_survey"]:
        flash("The survey is over!")
        return redirect('/thankyou')
    if index == 0:
        flash("Nice try, bro")
        return redirect(f"/questions/{index}")
    index -= 1
    session["current_index"] = index
    return redirect(f"/questions/{index}")

@app.route('/next')
def next():
    index = session["current_index"]
    if index == len(surveys[session["survey"]].questions)-1:
        flash("Nice try, bro")
        return redirect(f"/questions/{index}")
    index += 1
    session["current_index"] = index
    return redirect(f"/questions/{index}")
