from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('users.db')  
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
return render_template('reg.html')
    def login():

        if request.method == 'POST':
            username = request.form.get('username')  
            password = request.form.get('password')  

    
            conn = get_db_connection()
            conn.close()



if __name__ == '__main__':
    app.run(debug=True)