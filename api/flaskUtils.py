from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
import datetime

app = Flask(__name__)
CORS(app)

test_data = [
    {
        'date': '2021-04-24 07:30:02',
        'temp': 15750
    }
]

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/api/temps", methods=['GET'])
def getTemps():
    args = request.args
    
    try:
        conn = mysql.connector.connect(
            user='lance',
            password='l8rg8r',
            host='10.0.0.2',
            port=3306,
            database='laketemp'
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    
    cur = conn.cursor()

    if args['period'] == '24h':
        cur.execute('SELECT * FROM temps WHERE temps.date > DATE_SUB(CURDATE(), INTERVAL 1 DAY) ORDER BY temps.date desc;')
    elif args['period'] == '1y':
        cur.execute('SELECT * FROM temps WHERE temps.date > DATE_SUB(CURDATE(), INTERVAL 1 YEAR) ORDER BY temps.date desc;')
    else:
        return 'api request error. Check your period'

    res = []

    for (date,temp) in cur:
        res.append(
            {
                'timestamp': int(date.timestamp()),
                'temp': int(temp)
            }
        )

    conn.close()

    return jsonify(res)