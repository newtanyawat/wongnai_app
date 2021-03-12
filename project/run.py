from flask import redirect
from apps.server import app
from apps.routes import init_routes
from apps.dbconfig import *
import sys ,os

sys.path.append(".")

init_routes()

#todo หน้า upload success กด refesh แล้วส่งไฟล์ไปซ้ำ เพราะมันส่ง form อีกครั้ง ต้องแก้

@app.route('/')
def start():
    try :
        return redirect('/api/accounts/login')
    except Exception as e :
        return "path / is Error : " + str(e) 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=5000)
     