from flask import jsonify , request ,session,render_template ,redirect,render_template_string,make_response
from ..dbconfig import *
import os
from uuid import uuid4

def registor():
    try :
        return render_template('registor.html')
    except Exception as e :
        return "registor ERROR : " + str(e)


@connect_sqlite()
def service_registor(cursor):
    try :
        username = request.form['username']
        password = request.form['password']
        c_password = request.form['c_password']
        
        uuid = uuid4().__str__()[:8] # create unique id


        if username != '' and password==c_password and len(password) != 0: # password match and username not emptry
            into_accounts =   """
                        INSERT INTO accounts (uuid ,username, password)
                        VALUES (?,?,?);
                        """
            db_accounts = cursor.execute(into_accounts,(uuid,username, password)) 
            return redirect('/api/accounts/login')
        
        else:
            return render_template_string('<h1>password is incorrect!!!!</h1><br><button onclick="window.history.back()">Go Back</button>')
        
    except Exception as e :
        if str(e) == 'UNIQUE constraint failed: accounts.username' :
            return render_template_string('<h1>username is already being used !!!!</h1><br><button onclick="window.history.back()">Go Back</button>')
        return "service_registor ERROR : " + str(e)

def login():
    try :
        return render_template('login.html')
    except Exception as e :
        return "login ERROR : " + str(e)

def logout():
    try :
        session.pop('user_login' , None)
        session.pop('uuid_login' , None)
        return redirect('/api/accounts/login')
    except Exception as e :
        return "login ERROR : " + str(e)

@connect_sqlite()
def service_login(cursor):
    try :
        username = request.form['username']
        password = request.form['password']
        session.pop('user_login' , None)
        session.pop('uuid_login' , None)

        into_accounts = "SELECT uuid from accounts WHERE username=? AND password = ?"
        db_accounts = cursor.execute(into_accounts,(username, password))
        data = cursor.fetchone()[0]
        to_upload = '/api/files/upload/' + data
        if len(data) != 0 :
            session["user_login"] = username
            session["uuid_login"] = data
            # return render_template("file_upload.html", uuid = data , user_login = "test")
            return redirect('/api/files/upload')
        else :
            return render_template_string('<h1>OK PASS</h1><br><button onclick="window.history.back()">Go Back</button>')    
    except Exception as e :
        if str(e) == "'NoneType' object is not subscriptable":
            return render_template_string('''<h1>Username or Password is incorrect !!!!</h1><br>
                                        <button onclick="window.history.back()">Go Back</button>
                                        ''')
        return "service_login ERROR : " + str(e)