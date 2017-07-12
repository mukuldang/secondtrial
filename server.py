# echo_server.py
import socket
import xlwt
import subprocess
import os
import smtplib
from email import encoders
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import pdfkit
COMMASPACE = ', '
import sys
from random import randint
import urllib.request
from bs4 import BeautifulSoup
import os
import time
import json
from openpyxl import Workbook
import csv
host = 'ec2-52-15-225-210.us-east-2.compute.amazonaws.com'       # Symbolic name meaning all available interfaces
port = 5000     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
username="nchitaliya"
password="1234"
def emailing(send,passwo,topeople,subject):
    sender = send
    gmail_password = passwo
    recipients = topeople
        
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = ['fig.png','Results.pdf']

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

        # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


    
while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    data = conn.recv(10000)
    if data:   
        msg=data.decode('utf8')
        print(msg)
        msf=str(msg)
        a=msg.split(":")
        if a[0]=="excel":
            
            wb = Workbook()
            ws = wb.active
            
          
            b=a[1].split(",")
            
            for i in range(0,len(b)):
                ws.append([str(b[i])])
            wb.save("C:\\Users\\nchitaliya\\Desktop\\excel1.xlsx")
            conn.sendall(data)
        elif a[0]=="questions":
            b=a[2].split(",")
            with open('convertcsv.csv', 'w',newline='') as csvfile:
                fieldnames = ['body', 'body','type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(0,len(b)):
                    writer.writerow({'body': str(b[i]), 'body': str(b[i]),'type':'numeric'})
            dic={}
            for j in range(0,len(b)):
                if b[j]=="":
                    break
                dic[str(b[j])]='numeric'
            lst=[{'body':k,'type':v} for k,v in dic.items()]
            print(lst)
            x={'questions':lst,'title':str(a[1])}
            print (json.dumps(x, indent=2))
            with open('C:\\Users\\nchitaliya\\Desktop\\Twilio Project\\automated-survey-spring-master\\survey.json', 'w') as outfile:
                    json.dump(x, outfile)
            conn.sendall(data)
        elif a[0]=="password":
            b=a[1].split(",")
            if b[0]=="nchitaliya" and b[1]=="1234":
                m="True"
                conn.sendall(m.encode('utf8'))
            else:
                m="False"
                conn.sendall(m.encode('utf8'))
        elif a[0]=="True":
            try:
                os.system("x.bat")
            except:
                print("Port is open")
            p=subprocess.Popen(["python","script.py"])
           
            time.sleep(6)
            pids=p.pid
            os.system("java -jar runnable.jar")
            print("Letstry this")
            pdfkit.from_url('http://5c404705.ngrok.io/', 'Results.pdf')
            response=urllib.request.urlopen('http://5c404705.ngrok.io/')
            res=response.read()
            soup=BeautifulSoup(res)
            lis=[]
            lis1=[]
            ratings=[]
            count=1
            for i in soup.find_all('li'):
                lis.append(i.text)
            for i in range(4,len(lis)):
                if i%4==0:
                    a=lis[i].split(": ")
                    lis1.append(a[1])
                if i-count==4:
                    count=i
                    a=lis[i].split(": ")
                    u=a[1].rstrip("\n ")
                    if int(u)>5:
                        ratings.append(str(5))
                    ratings.append(str(u))
            dic={}
            key=[]
            print("This is the lis")
            print(lis[4:])
            print("This is the ratings we got")
            print(ratings)
            with open("C:\\Users\\nchitaliya\\Desktop\\callfile.txt","r") as f:
                for line in f:
                    b=line.split("=")
                    dic[str(b[1]).strip("\n")]=str(b[0])
                    key.append(str(b[1]).strip("\n"))
            count=0
            msg=""
            for i in range(0,len(key)):
                if key[i] not in lis1:
                    msg=msg+dic[key[i]]+","
                    count=count+1
            #if(msg==""):
            #    msg="NONE"
            #    conn.send(msg.encode('utf8'))
            conn.send(msg.encode('utf8'))
            realrating=[ratings.count("1"),ratings.count("2"),ratings.count("3"),ratings.count("4"),ratings.count("5"),count]
            msg1=""
            for i in range(0,len(realrating)):
                msg1=msg1+str(realrating[i])+","
            print(msg)
            print(msg1)
            conn.send(msg1.encode('utf8'))
            w=open("C:\\Users\\nchitaliya\\Desktop\\callfile.txt","w")
            w.close()
            
            try:
                os.system("x.bat")
            except:
                print("Port is open")
            
            p.terminate()

            
            
        
            print("HELLLLOOOOOOOOOOOOOOOOOOOO")
        elif a[0]=="rating":
            objects = ('Rating 1', 'Rating 2', 'Rating 3', 'Rating 4', 'Rating 5 \nor more', 'No \nResponse')
            y_pos = np.arange(len(objects))
            rating=a[1].split(',')
            rating.pop(len(rating)-1)
            plt.bar(y_pos, rating, align='center', alpha=0.5)
            plt.xticks(y_pos,objects)
            print(rating)
            plt.ylabel('Number of Responses')
            plt.title('Results for your survey!')
            plt.savefig('fig.png')
            emailing("lorddarkseid08@gmail.com","Mukul123",["mukul94dang@gmail.com"],"Your Survey Results")
       

    
            
            
 



