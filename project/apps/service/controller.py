from flask import (Flask,render_template,session,request,redirect,flash,url_for, send_from_directory,render_template_string )
from datetime import datetime , timedelta
from ..dbconfig import *
import os , pytz
from uuid import uuid4
 
config = {"max_content" : 104857600 }

from datetime import datetime, timezone, timedelta


tz = pytz.timezone('Asia/Bangkok')
x1 = datetime.now(tz)
# Create UTC date objects
x2 = datetime.now(tz) + timedelta(minutes=7)
print(x1 , x2)
print(x1 < x2)

def upload():
    try :
        return render_template('file_upload.html' , uuid = session["uuid_login"] , user_login = session["user_login"])
    except Exception as e :
        rtn ='''<h1>You are not logged in !!!.</h1><br>
                    <p><h2>link login : <a href="/{0}">{1}{0} </a></h2></p><br>
                    '''.format('api/accounts/login',request.host_url)
        return render_template_string(rtn)
       
        
@connect_sqlite()
def service_upload(cursor):
    try:
        login_user = session["user_login"]
        src_file = request.files['file']
        password = request.form['password']
        download = request.form['download']
        expDate = request.form['expDate']
        uuid = request.form['uuid'] 
        exp_date = datetime.now() + timedelta(hours=7,minutes=int(expDate)) #วันหมดอายุไฟล์ #! +7 ชม. เพราะเมื่อขึ้น docker แล้วเวลา -7 ชม.
        create_at = datetime.now() + timedelta(hours=7) #วันสร้างไฟล์ #! +7 ชม. เพราะเมื่อขึ้น docker แล้วเวลา -7 ชม.

        if request.content_length > config["max_content"] :
            return render_template_string('<h1> Upload fail : more than limit file !!!!</h1><br><button onclick="window.history.back()">Go Back</button>')
        if src_file.filename == '':
            return render_template_string('<h1> Upload fail : No selected file !!!!</h1><br><button onclick="window.history.back()">Go Back</button>')
        if request.files :
            uuid_file = uuid4().__str__()[:8] # id file
            file_name = src_file.filename # realname
            uuid_name = uuid_file + "-" + file_name
            src_file.save(os.path.join("upload/",uuid_name))
            into_files =   """
            INSERT INTO files (uuid ,name, uuid_name,password,download_times,create_by,create_at,exp_at)
            VALUES (?,?,?,?,?,?,?,?)"""
            db_files = cursor.execute(into_files ,(uuid_file , file_name , uuid_name , password ,int(download) , session["user_login"] , create_at ,exp_date ))
            rtn = '''<h1> UPLOAD SUCCES</h1><br>
                    <p><h2>link download : <a href="{3}{0}/{2}">{3}{0}/{2} </a></h2></p><br>
                    <p><h2>link delete   : <a href="{3}{1}/{2}">{3}{1}/{2}</a></h2></p><br>
                    '''.format('api/files/download','api/files/delete',uuid_name,request.host_url)
            return rtn
    except Exception as e:
        return "serive_upload ERROR : "+str(e)

@connect_sqlite()
def download(cursor,uuid_name):
    try :
        rtn = 'SELECT password from files WHERE uuid_name="{0}"'.format(uuid_name)
        db_files = cursor.execute(rtn)
        data = cursor.fetchone()[0]
        if len(data) != 0:
            passwordTF = True
        else :
            passwordTF = False
        return render_template('file_download.html', uuid_name = uuid_name , password = passwordTF)
    except Exception as e :
        #! check files has been delete!!
        if str(e) == "'NoneType' object is not subscriptable" :
            return render_template_string('<h1> File has been deleted. !!!!</h1>')
        else :
            return "download ERROR : "+str(e)

@connect_sqlite()
def service_download(cursor,uuid_name):
    try :
        rtn = 'SELECT name , password , download_times , create_at , exp_at from files WHERE uuid_name="{0}"'.format(uuid_name)
        db_files = cursor.execute(rtn)
        data = cursor.fetchall()
        old_name = data[0][0]
        password = data[0][1]
        download_times = int(data[0][2])
        create_at = data[0][3]
        exp_date = data[0][4]

        #! ตรวจสอบไฟล์หมดเวลา exp_at 
        files_timeUP = str(datetime.now()) > exp_date

        #! No password file
        if request.form :   #password file
            rq_password = request.form['password']
            # if password == rq_password and download_times != 0  :
            if password == rq_password and download_times != 0 and files_timeUP  == False :
                reduce_times(uuid_name)
                return send_from_directory('../upload',filename = uuid_name, as_attachment=True, attachment_filename=old_name)
            elif download_times == 0 :
                return render_template_string('<h1> File Timeout !!!!</h1><br><button onclick="window.history.back()">Go Back</button>')
            else :
                return render_template_string('<h1> PASSWORD INCONRECT !!!!</h1><br><button onclick="window.history.back()">Go Back</button>')
        
        #! No password file
        elif download_times != 0 :              
            reduce_times(uuid_name)
            return send_from_directory('../upload',filename = uuid_name, as_attachment=True, attachment_filename=old_name)
        elif download_times == 0 :
            return render_template_string('<h1> File Timeout !!!!</h1><br><button onclick="window.history.back()">Go Back</button>')
        else :
            return render_template_string('<h1> Download FILE ERROR !!!!</h1><br><button onclick="window.history.back()">Go Back</button>')
    except Exception as e :
        return "service_download ERROR" + str(e)

def delete(uuid_name):
    try :
        return render_template('file_delete.html' , uuid_name = uuid_name )
    except Exception as e :
        return "delete ERROR : "+str(e)

@connect_sqlite()
def confirm_delete(cursor,uuid_name):
    try :
        session["user_login"]
        return render_template('confirm_delete.html' , uuid_name = uuid_name )
    except Exception as e :
        rtn ='''<h1>If you want to delete this file. Please login !!!.</h1><br>
                    <p><h2>link login : <a href="/{0}">{1}{0} </a></h2></p><br>
                    '''.format('api/accounts/login',request.host_url)
        return render_template_string(rtn)


@connect_sqlite()
def service_delete(cursor,uuid_name):
    try :
        if session["user_login"] != None :
            #find create by
            rtn = 'SELECT create_by from files WHERE uuid_name="{0}"'.format(uuid_name)
            db_files = cursor.execute(rtn)
            data = cursor.fetchone()[0]     

            if data == session["user_login"] :
                #delete from database
                delete = 'delete FROM files WHERE uuid_name="{0}"'.format(uuid_name)
                cursor.execute(delete)

                #delete from local
                path_delete = 'upload/'
                delete_name = uuid_name
                delete_file = path_delete+delete_name
                os.remove(delete_file)
                return redirect("/api/files/upload")
            else :
                return render_template_string('<h1> Only the owner can delete this file.!!!!</h1>')
        else :
            rtn ='''<h1>If you want to delete this file. Please login !!!.</h1><br>
                    <p><h2>link login : <a href="/{0}">{1}{0} </a></h2></p><br>
                    '''.format('api/accounts/login',request.host_url)
            return render_template_string(rtn)    
    except Exception as e :
        #! check files has been delete!!
        error = str(e).split()
        checkEmtry = error[0]+error[1]
        if checkEmtry == "[WinError2]" :
            return render_template_string('<h1> File has been deleted. !!!!</h1>')
        elif str(e) == "'NoneType' object is not subscriptable" :
            return render_template_string('<h1> File has been deleted. !!!!</h1>')
        else :
            return "service_delete ERROR : "+str(e)
        

@connect_sqlite()
def reduce_times(cursor,uuid_name):
    try :
        reduce_times = 'UPDATE files SET download_times = download_times -1 WHERE uuid_name = "{0}"'.format(uuid_name)
        rd_times = cursor.execute(reduce_times)
    except Exception as e :
        return "reduce times ERROR" + str(e)

@connect_sqlite()
def list_files(cursor):
    try :
        cursor.execute("select * from files")
        rows = cursor.fetchall(); 
        return render_template('file_list.html', rows = rows)
    except Exception as e :
        return "list_files ERROR : "+ str(e)