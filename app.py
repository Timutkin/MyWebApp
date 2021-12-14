import requests
from flask import Flask, render_template, request, redirect, flash
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdf23432rfewdsvc214tgfweds'
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="09fiveva",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if str(password) == "" and str(username) == '':
                flash('Username and password not entered')
            elif str(username) != '' and str(password) == '':
                flash('Password not entered')
            elif str(username) == '' and str(password) != '':
                flash('Username not entered')
            else:
                try:
                    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
                    records = list(cursor.fetchall())
                    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
                except:
                    flash('Data missing in database')
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if len(name) < 2 or len(login) < 6 or len(password) < 5:
            flash('The name must be at least two characters long, the login must be at least 6 characters, and the password must be at least four characters')
        else:
            flag = True
            cursor.execute("SELECT login FROM service.users ")
            logins = list(cursor.fetchall())
            for el in logins:
                if str(el)[2:len(str(el))-3] == login:
                    flash('User with this login already exists')
                    flag = False
                    break
            if flag:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(name), str(login), str(password)))
                conn.commit()
                print("The user has been added to the database")
                return redirect('/login/')

    return render_template('registration.html')
