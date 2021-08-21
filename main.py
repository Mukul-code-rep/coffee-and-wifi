from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps', validators=[DataRequired(), URL(message='Please enter a URL')])
    opening = StringField('Opening Time', validators=[DataRequired()])
    closing = StringField('Closing Time', validators=[DataRequired()])
    choice_coffee = [('☕️', '☕️'), ('☕️☕️', '☕️☕️'), ('☕️☕️☕️', '☕️☕️☕️'), ('☕️☕️☕️☕️', '☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')]
    coffee = SelectField('Coffee Rating', choices=choice_coffee, validators=[DataRequired()])
    wifi_choice = [('💪', '💪'), ('💪💪', '💪💪️'), ('💪️💪️💪️', '💪💪💪️'), ('💪️💪️💪️💪️', '💪💪💪💪️'), ('💪️💪️💪️💪️💪️', '💪💪💪💪💪️')]
    wifi = SelectField('WiFi Strength Rating', choices=wifi_choice, validators=[DataRequired()])
    socket_choice = [('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')]
    socket = SelectField('Power Socket Availability', choices=socket_choice, validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = form.data
        data = []
        for key in new_cafe:
            data.append(new_cafe[key])
        with open('cafe-data.csv', mode='a') as f:
            writer = csv.writer(f)
            writer.writerow(data[:7])
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
