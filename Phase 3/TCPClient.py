# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 20:30:51 2016

@author: Tracy Marshall
"""

import socket
import ssl
#import rsa
import os.path
#import rsa
import pickle

TCP_IP = "192.168.0.162"
HOST = ''
TCP_PORT = 50021
BUFFER_SIZE = 1024
MESSAGE = "Hello Mate!"

ip = "192.168.0.162"
port = 50021


def client(ip, port, message):
   s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   ssl_sock = ssl.wrap_socket(s,
                              ca_certs="TFMS.crt",
                              cert_reqs=ssl.CERT_REQUIRED,
                              ssl_version=ssl.PROTOCOL_TLSv1)
   ssl_sock.connect((ip,port))
   try:
      ssl_sock.send(message)
      response = ssl_sock.recv(4096)
      print "Received: {}".format(response)
   finally:
      ssl_sock.close()
    
    
while True:

   option = raw_input("1 - Add User\n" \
                      "2 - Modify User\n"\
                      "3 - Add Results\n"\
                      "4 - Update Status\n")
                      
   senderName = raw_input("Enter your name: ")
   senderID = raw_input("Enter your ID: ")
                      
   if option == "1":
   
      newUserType = raw_input("Enter users type: ")
      newUserName = raw_input("Enter users name: ")
      newUserID = raw_input("Enter users id: ")
      newUserTeam = raw_input("Enter users team: ")
      newUserGender = raw_input("Enter users gender: ")
   
      client(ip, port, pickle.dumps(["adduser", senderName, senderID, newUserType, newUserName, newUserID, newUserTeam, newUserGender]))
   
   elif option == "2":
   
      oldUserName = raw_input("Enter name of user to be modified: ")
      oldUserID = raw_input("Enter id of user to be modified: ")
      newUserType = raw_input("Enter users type: ")
      newUserName = raw_input("Enter users name: ")
      newUserID = raw_input("Enter users id: ")
      newUserTeam = raw_input("Enter users team: ")
      newUserGender = raw_input("Enter users gender: ")
      
      client(ip, port, pickle.dumps(["modifyuser", senderName, senderID, oldUserName, oldUserID,  newUserType, newUserName, newUserID, newUserTeam, newUserGender]))
   
   
   elif option == "3":
   
      eventID = raw_input("Enter event ID: ")
      athleteName = raw_input("Enter athlete name: ")
      athleteID = raw_input("Enter athlete ID: ")
      athleteTeam = raw_input("Enter athlete team: ")
      attempt = raw_input("Enter attempt number (zero if n/a): ")
      value = raw_input("Enter result value: ")
   
      client(ip, port, pickle.dumps(["addresults", senderName, senderID, eventID, athleteName, athleteID, athleteTeam, attempt, value]))
   
   elif option == "4":
   
      eventID = raw_input("Enter event ID: ")
      athleteName = raw_input("Enter athlete name: ")
      athleteID = raw_input("Enter athlete ID: ")
      status = raw_input("Enter status: ")
      
   
      client(ip, port, pickle.dumps(["updatestatus", senderName, senderID, eventID, athleteName, athleteID, status]))
   
# response = raw_input("Start? ")
# print("First message...")      
# client(ip, port, pickle.dumps(["hello", "world", "1"]))
# response = raw_input("Continue? ")
# print("Second message...")   
# client(ip, port, pickle.dumps(["updatestatus", "tracy", "12345", "200", "sarah", "98989", "at event"]))
# #client(ip, port, pickle.dumps(["adduser", "tracy", "12345", "coach", "tina", "98000", "wichita", "female"]))
# #client(ip, port, pickle.dumps(["addresults", "jimmie", "55555", "345", "steve", "77777", "hutchinson", "3", "9.04"]))
# response = raw_input("Continue? ")


   
