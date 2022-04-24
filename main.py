from flask import Flask, render_template
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Han6some_pe1verts'


@app.route('/register', methods=['GET', 'POST'])
def register():# Дописать код проверки данных из формы, добавления в бд, и перенаправления на главный сайт
    form = RegisterForm()
    if form.validate_on_submit():
        return render_template("main.html")

    return render_template('register.html',form=form)



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')