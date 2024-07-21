from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, url
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '3FA9812D1B3F183GS131BFSADAFB10F4451'
Bootstrap5(app)

COFFEE_RATINGS = ["✘", "☕️", "☕️☕️️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"]
WIFI_RATINGS = ["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
POWER_RATINGS = ["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location URL', validators=[DataRequired(), url()])
    open = StringField('Open time', validators=[DataRequired()])
    close = StringField('Close time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=COFFEE_RATINGS)
    wifi_rating = SelectField('Wifi Rating', validators=[DataRequired()], choices=WIFI_RATINGS)
    power_rating = SelectField('Power Rating', validators=[DataRequired()], choices=POWER_RATINGS)
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        row = [form.cafe.data, form.location_url.data, form.open.data, form.close.data,
               form.coffee_rating.data, form.wifi_rating.data, form.power_rating.data]
        with open("cafe-data.csv", "a", encoding="utf-8", newline='') as file:
            csv.writer(file).writerow(row)

        return redirect("/cafes")

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template('cafes.html',
                           cafes=list_of_rows, nof_labels=len(list_of_rows[0]), nof_rows=len(list_of_rows))


if __name__ == '__main__':
    app.run(debug=True)
