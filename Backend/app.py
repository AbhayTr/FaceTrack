import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import socket
import logging
import os
import signal
import sqlite3
from sqlite3 import Error
import cv2
import numpy as np
import io
import base64
from PIL import Image
from datetime import datetime
import time
import threading
import csv

lock = threading.Lock()

logging.getLogger("tornado.access").disabled = True
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn, create_table_sql):
    c = conn.cursor()
    c.execute(create_table_sql)

def read_b64(uri):
   encoded_data = uri.split(",")[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

class Application(tornado.web.Application):
        
    def __init__(self):
        handlers = [(r"/", MainHandler)]
        settings = dict(debug = True)
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.websocket.WebSocketHandler):

    conn = None
    id = None
    wfps = None
    sampleNum = 0
    found = False
    udata = []

    def check_origin(self, origin):
        return True
    
    def open(self):
        try:
            self.conn = create_connection("data/attendance.db")
        except Error as sql_error:
            raise RuntimeError(f"An SQL error occured from one of the connections. Log: {str(sql_error)}.)")
    
    def on_close(self):
        try:
            self.conn.close()
        except:
            pass

    def on_message(self, data):
        try:
            lock.acquire()
            if "[DATA]" in data:
                data = data.replace("[DATA]", "")
                register_data = data.split(",")
                self.id = register_data[0]
                cmd = "SELECT * FROM students WHERE id = '" + str(self.id) + "';"
                cursor = self.conn.execute(cmd)
                isRecordExist = False
                for row in cursor:
                    isRecordExist = True
                if isRecordExist:
                    cmd = "UPDATE students SET name = '" + str(register_data[1]) + "' WHERE id = '" + str(self.id) + "';"
                    cmd2 = "UPDATE students SET section = '" + str(register_data[2]) + "' WHERE id = '" + str(self.id) + "';"
                    cmd3 = "UPDATE students SET branch = '" + str(register_data[3]) + "' WHERE id = '" + str(self.id) + "';"
                    cmd4 = "UPDATE students SET program = '" + str(register_data[4]) + "' WHERE id = '" + str(self.id) + "';"
                    self.conn.execute(cmd)
                else:
                    params = (self.id, register_data[1], register_data[2], register_data[3], register_data[4], 0)
                    cmd = "INSERT INTO students(id, name, section, branch, program, previous_marked) VALUES(?, ?, ?, ?, ?, ?)"
                    cmd2 = ""
                    cmd3 = ""
                    cmd4 = ""
                    self.conn.execute(cmd, params)
                self.conn.execute(cmd2)
                self.conn.execute(cmd3)
                self.conn.execute(cmd4)
                self.conn.commit()
                self.conn.close()
                self.write_message("S1")
            elif "[CLEAR]" in data:
                if self.wfps == None:
                    self.write_message("IE")
                else:
                    today = str(int(time.time()))
                    cmd = "UPDATE students SET previous_marked = " + today + " WHERE id = '" + str(self.wfps) + "';"
                    cursor = self.conn.execute(cmd)
                    self.conn.commit()
                    self.conn.close()
                    self.wfps = None
                    data_rows = ("Reg. No.", "Name", "Section", "Branch", "Program", "Previously_Accessed_At")
                    self.udata = (self.udata[0], self.udata[1], self.udata[2], self.udata[3], self.udata[4], datetime.fromtimestamp(int(today)).strftime("%d-%m-%Y"))
                    header_write = False
                    if not os.path.exists("data/attendance.csv"):
                        header_write = True
                    with open("data/attendance.csv", "a") as datafile:
                        if header_write:
                            csvwriter = csv.writer(datafile)
                            csvwriter.writerow(data_rows)
                        csvwriter = csv.writer(datafile)
                        csvwriter.writerow(self.udata)
                        datafile.close()
                    self.udata = []
                    self.write_message("AMS " + today)
            else:
                if self.id != None:
                    if self.sampleNum <= 100:
                        img = read_b64(data)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = face_detector.detectMultiScale(gray, 1.3, 5)
                        if len(faces) > 1:
                            self.write_message("MFD")
                        else:
                            for (x, y, w, h) in faces:
                                self.sampleNum += 1
                                cv2.imwrite("dataSet/student." + str(self.id) + "." + str(self.sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    else:
                        recognizer = cv2.face.LBPHFaceRecognizer_create()
                        try:
                            recognizer.read("data/studentFacialData.yml")
                        except:
                            pass
                        path = "dataSet"
                        imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
                        faces = []
                        ids = []
                        for imagepath in imagepaths:
                            if ".DS_Store" in imagepath or "desc.txt" in imagepath:
                                continue
                            else:
                                face_img = Image.open(imagepath).convert("L")
                                face_np = np.array(face_img, "uint8")
                                cid = int(os.path.split(imagepath)[-1].split(".")[1])
                                faces.append(face_np)
                                ids.append(cid)
                                os.remove(imagepath)
                        ids = np.array(ids)
                        recognizer.update(faces, ids)
                        recognizer.save(f"data/studentFacialData.yml")
                        self.id = None
                        self.sampleNum = 0
                        self.write_message("RC")
                else:
                    if not self.found:
                        recognizer = cv2.face.LBPHFaceRecognizer_create()
                        recognizer.read("data/studentFacialData.yml")
                        img = read_b64(data)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = face_detector.detectMultiScale(gray, 1.3, 5)
                        student_data = []
                        if len(faces) > 1:
                            self.write_message("MFD")
                        else:
                            for (x, y, w, h) in faces:
                                cid, conf = recognizer.predict(gray[y : y+h, x : x+w])
                                cmd = "SELECT * FROM students WHERE id = '" + str(cid) + "';"
                                cursor = None
                                try:
                                    cursor = self.conn.execute(cmd)
                                except:
                                    self.conn = create_connection("data/attendance.db")
                                    cursor = self.conn.execute(cmd)
                                for row in cursor:
                                    student_data = row
                        if student_data != []:
                            self.found = True
                            if (datetime.now() - datetime.fromtimestamp(student_data[5])).days == 0:
                                self.write_message(f"{student_data[0]},{student_data[1]},{student_data[2]},{student_data[3]},{student_data[4]},{student_data[5]}")
                            else:
                                self.wfps = cid
                                self.udata = student_data
                                self.write_message(f"{student_data[0]},{student_data[1]},{student_data[2]},{student_data[3]},{student_data[4]}")
                        else:
                            self.write_message("UNK")
            lock.release()
        except Error as sql_error:
            try:
                lock.release()
            except:
                pass
            try:
                self.write_message("500")
            except:
                pass
            raise RuntimeError(f"An SQL error occured from one of the connections during messaging. Log: {str(sql_error)}.")
        except Exception as error:
            try:
                lock.release()
            except:
                pass
            try:
                self.write_message("500")
            except:
                pass
            raise RuntimeError(f"An error occured. Log: {str(error)}.")
            
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    try:
        create_connection("data/attendance.db")
        sql_create_students_table = """ CREATE TABLE IF NOT EXISTS students (
                                        id text PRIMARY KEY,
                                        name text NOT NULL,
                                        section text NOT NULL,
                                        branch text NOT NULL,
                                        program text NOT NULL,
                                        previous_marked integer NOT NULL
                                    ); """
        conn = create_connection("data/attendance.db")
        if conn is not None:
            create_table(conn, sql_create_students_table)
            conn.close()
        else:
            raise RuntimeError("Error! cannot create the database connection.")
        private_ip_address = socket.gethostbyname(socket.gethostname())
        app.listen(8000, address = "0.0.0.0")
        print(f"\nFaceTrack is LIVE and is accessible at '{private_ip_address}:8000'!")
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print()
        try:
            os.kill(os.getpid(), signal.SIGKILL)
        except:
            os.kill(os.getpid(), signal.SIGABRT)
    except Error as sql_error:
        try:
            lock.release()
        except:
            pass
        print(f"An SQL error occured. Log: {str(sql_error)}.")
    except Exception as error:
        try:
            lock.release()
        except:
            pass
        print(f"An error occured. Log: {str(error)}.")