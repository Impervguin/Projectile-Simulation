from flask import Flask, render_template, redirect, request
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
import plotly
import plotly.express as px
from data import db_session
from data.users import User
from data.user_graphs import UserGraphs
from calculate_coordinates import *
import InternSysConverter

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'Han6some_pe1verts'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/main")
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
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        login_user(user, remember=False)
        return redirect('/main')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/main")
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect("/main")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/physical_values')
def physical_values():
    if not current_user.is_authenticated:
        return redirect("/")
    data = DATA
    return render_template('physical_values.html', data=data)


@app.route('/theory')
def theory():
    if not current_user.is_authenticated:
        return redirect("/")
    return render_template("theory.html")


@app.route('/main')
def main():
    if not current_user.is_authenticated:
        return redirect("/")

    db_sess = db_session.create_session()
    graphs = sorted([i.to_dict() for i in db_sess.query(UserGraphs).all()], key=lambda x: x['id'])

    fig = plotly.graph_objs.Figure()
    for graph in graphs:
        if graph["resistance"]:
            req_data = ["speed", "angle", "planet", "height", "air_env", "substance", "mass", "calc_step"]
            data = {}
            for elem in req_data:
                data[elem] = graph[elem]
            x, y, t = calculate_with_air_resistance(**data)
        else:
            req_data = ["speed", "angle", "planet", "height", "calc_step"]
            data = {}
            for elem in req_data:
                data[elem] = graph[elem]
            x, y, t = calculate_without_air_resistance(**data)
        fig.add_scatter(x=x, y=y, mode="lines", name=str(graph["id"]))
    fig.update_xaxes(title_text="X, метры")
    fig.update_yaxes(title_text="Y, метры")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("main.html", projectiles=graphs, graphJSON=graphJSON)


@app.route('/postdata', methods=["post"])
@login_required
def postdata():
    db_sess = db_session.create_session()
    reqdata = dict(request.form)
    for key in reqdata.keys():
        if key == 'speed':
            reqdata[key] = InternSysConverter.get_speed_in_metersps(reqdata[key])
        elif key == 'mass':
            reqdata[key] = InternSysConverter.get_mass_in_kilograms(reqdata[key])
        elif key == 'angle':
            reqdata[key] = InternSysConverter.get_angle_in_degrees(reqdata[key])
        elif key == 'resistance':
            reqdata[key] = bool(reqdata[key])
        elif key not in {'air_env', 'planet', 'substance'}:
            reqdata[key] = float(reqdata[key])
    graph = UserGraphs(**reqdata)
    current_user.user_graphs.append(graph)
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect("/main")


@app.route('/deleteall')
@login_required
def deleteall():
    db_sess = db_session.create_session()
    graphs = db_sess.query(UserGraphs).filter(UserGraphs.user == current_user).all()
    for i in graphs:
        db_sess.delete(i)
        db_sess.commit()
    return redirect("/main")


@app.route('/delete_graph', methods=["post"])
@login_required
def delete_graph():
    _id = request.data  # Undefined behavior, probably unexpected type.
    print(_id)
    db_sess = db_session.create_session()
    graph = db_sess.query(UserGraphs).filter(UserGraphs.user == current_user, UserGraphs.id == _id).first()
    if graph:
        db_sess.delete(graph)
        db_sess.commit()
    return redirect("/main")


@app.route("/")
def start():
    if current_user.is_authenticated:
        return redirect("/main")
    return render_template("start.html")


@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect("/")
    logout_user()
    return redirect("/")


def startup():
    db_session.global_init("db/users_information.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    startup()
