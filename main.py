from flask import Flask, render_template, redirect
from forms.user import RegisterForm, LoginForm
import pandas as pd
import json
import plotly
import plotly.express as px
from data import db_session
from data.users import User
from data.read_constants import transfer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Han6some_pe1verts'
DATA = transfer()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_confirmation.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message="Такой пользователь уже есть")
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect("/main")
    return render_template('login.html', form=form)


@app.route('/physical_values')
def physical_values():
    data = DATA
    return render_template('physical_values.html', data=data)

@app.route('/theory')
def theory():
   return render_template("theory.html")


@app.route('/main')
def main():
    df = pd.DataFrame({
        'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges',
                  'Bananas'],
        'Amount': [4, 1, 2, 2, 4, 5],
        'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']})
    fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("main.html", graphJSON=graphJSON)


if __name__ == '__main__':
    db_session.global_init("db/users_information.db")
    app.run(port=8080, host='127.0.0.1')
