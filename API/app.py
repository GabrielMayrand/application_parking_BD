from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

#Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'application_parking'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if(request.method=='GET'):
        cur = mysql.connection.cursor()
        utilisateurs = cur.execute("SELECT * FROM utilisateur")
        utilisateurs = cur.fetchall()
        return jsonify(utilisateurs)

if __name__ == '__main__':
    app.run(debug=True)