import psycopg2
from flask import Flask, render_template, request, redirect
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

DB_HOST = "172.27.128.1"
DB_NAME = "test_chart"
DB_USER = "postgres"
DB_PASS = "1"


def get_db_connect():
    return psycopg2.connect(
        host=DB_HOST,
        port=5432,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


@app.route('/')
@cross_origin(origin='*')
def index():
    return render_template("index.html")


@app.route('/submit', methods=['POST', ])
@cross_origin(origin='*')
def submit():
    name = request.form['name']
    cost = request.form['cost']
    quantity = request.form['quantity']
    conn = get_db_connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO web_input (name, cost, quantity) VALUES (%s, %s, %s)', (name, cost, quantity))
    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/output')
@cross_origin(origin='*')
def output():
    conn = get_db_connect()
    cur = conn.cursor()
    cur.execute('SELECT name, cost, quantity FROM web_input')
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('output.html', users=data)


@app.route('/monitor')
@cross_origin(origin='*')
def monitor():
    return redirect('http://localhost:3000')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
