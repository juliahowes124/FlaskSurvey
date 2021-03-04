from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def index():
    title = survey.title
    instructions = survey.instructions
    return render_template('survey_start.html', title=title, instructions=instructions)


@app.route('/begin', methods=["POST"])
def begin():
    return redirect('/questions/0')


@app.route('/questions/<int:index>')
def questions(index):
    question = survey.questions[index]

    return render_template(
        "question.html",
        question=question
    )


@app.route('/answer', methods=["POST"])
def answer():
    responses.append(request.form["answer"])
    index = len(responses)
    if index >= len(survey.questions):
        return redirect('/thankyou')
    return redirect(f"/questions/{index}")


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
