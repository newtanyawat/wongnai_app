from flask import redirect
from apps.server import app
from apps.dbconfig import *
import threading
from datetime import datetime , timedelta
import sys ,os

sys.path.append(".")

dateNOW = datetime.now() + timedelta(hours=7) #! +7 ชม. เพราะเมื่อขึ้น docker แล้วเวลา -7 ชม.

@app.route('/')
@connect_sqlite()
def start(cursor):
    try :
        
        rtn = 'SELECT uuid_name , exp_at from files'
        db_files = cursor.execute(rtn)
        data = cursor.fetchall()

        for col in data :
            data_01 = col
            compare = str(dateNOW) > data_01[1] 
            if compare == True :
                #! delete form DB 
                delete = 'delete FROM files WHERE uuid_name="{0}"'.format(data_01[0])
                cursor.execute(delete)
                # print(data_01[0] , compare )

                #! delete from local 
                file_name = data_01[0]
                path_file = "../project/upload/"
                delete_file = path_file + file_name
                # print(delete_file)
                os.remove(delete_file)
        return "service delete time is working"
    except Exception as e :
        return "service delete time Error : " + str(e) 



@connect_sqlite()
def time_delete_files(cursor):
    try :
        rtn = 'SELECT uuid_name , exp_at from files'
        db_files = cursor.execute(rtn)
        data = cursor.fetchall()

        for col in data :
            data_01 = col
            compare = str(dateNOW) > data_01[1] 
            if compare == True :
                #! delete form DB 
                delete = 'delete FROM files WHERE uuid_name="{0}"'.format(data_01[0])
                cursor.execute(delete)

                #! delete from local 
                file_name = data_01[0]
                path_file = "../project/upload/"
                delete_file = path_file + file_name
                os.remove(delete_file)
        # print("service time delete is working")
    except Exception as e :
        return "service delete time Error : " + str(e) 


interval = 300

def startTimer():
    threading.Timer(interval, startTimer).start()
    time_delete_files()

startTimer()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=4005)
     