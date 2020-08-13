from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = []


@app.route('/')
def to_home():
    return render_template("to_survey.html", survey=survey)


@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session['RESPONSES_KEY'] = []


    return redirect("/question/0")

@app.route("/question/<int:id>")
def show_question(id):

    responses = session.get('RESPONSES_KEY')

    if (len(responses) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/question/{len(responses)}")

    question = survey.questions[id]
    return render_template("question.html", question_num=id, question=question)

@app.route("/answer", methods=["POST"])
def answers():

    respon = session['RESPONSES_KEY']

    choice = request.form.get('answer')
    if not choice:
        return redirect(f"/question/{len(respon)}")
    
    respon.append(choice)
    session['RESPONSES_KEY'] = respon

    if len(survey.questions) == len(respon):
        return redirect("/complete")
    return redirect(f"/question/{len(respon)}")


@app.route("/complete")
def to_complete():

    return render_template("complete.html",survey = survey, res=session['RESPONSES_KEY'])

