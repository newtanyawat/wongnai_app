from flask import redirect
from apps.server import app
from apps.dbconfig import *
import threading
import sys ,os

sys.path.append(".")

@app.route('/')
@connect_sqlite()
def start(cursor):
    try :
        delete_file = "../project/upload/tanyawat.txt"
        # os.remove(delete_file)
        rtn = 'SELECT uuid_name , exp_at from files'
        db_files = cursor.execute(rtn)
        data = cursor.fetchall()
        # print(list(data))
        print(data)
        for col in data :
            data_01 = col
            print("uuid_name")
        print(data_01[0])
        print(data_01[1])
        return "test is working"
    except Exception as e :
        return "path / is Error : " + str(e) 

# def time_delete_files():
#   threading.Timer(300.0, printit).start()
#   #!ถามแววเรื่องการระบุ path ต้องการลบไฟล์จาก folder upload ของ Project
#   #Todo query selete exp_at , uuid from files database every 5 munite and looking col : exp_at and compare dateNow() > exp_at => if true delete files from local and database
#   rtn = "selecet uuid , uuid_name , exp_at from files"

# time_delete_files()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=4005)
     