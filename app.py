from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from mailgun import Mailgun
from dotenv import load_dotenv



app = Flask(__name__)


db = SQLAlchemy(app)

load_dotenv("../feedback_form/.env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    date = db.Column(db.Date)
    guid = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)

    def __init__(self, customer, date, guid, rating, comments):
        self.customer = customer
        self.date = date
        self.guid = guid
        self.rating = rating
        self.comments = comments

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        date = request.form['date']
        guid = request.form['guid']
        rating = request.form['rating']
        comments = request.form['comments']
        if customer == '' or guid == '' or date == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, date, guid, rating, comments)
            data.save_to_db()
            html = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Date: {date}</li><li>Guid: {guid}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"
            Mailgun.send_email(html)
            return render_template('success.html', name=customer)
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run(port=5000)


