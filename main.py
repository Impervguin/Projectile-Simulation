from flask import Flask, render_template, redirect
from forms.user import RegisterForm, LoginForm
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Han6some_pe1verts'


@app.route('/register', methods=['GET', 'POST'])
def register():# Дописать код проверки данных из формы, добавления в бд, и перенаправления на главный сайт
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect("/main")
    return render_template('register.html',form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect("/main")
    return render_template('login.html', form=form)

@app.route('/main')
def notdash():
   df = pd.DataFrame({
      'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges',
      'Bananas'],
      'Amount': [4, 1, 2, 2, 4, 5],
      'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']})
   fig = px.bar(df, x='Fruit', y='Amount', color='City',barmode='group')
   graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
   return render_template("main.html", graphJSON=graphJSON)
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')