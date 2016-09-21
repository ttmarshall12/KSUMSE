# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 20:30:51 2016

@author: Tracy Marshall
"""

import socket
import rsa
import os.path
#import rsa

TCP_IP = '192.168.0.113'
HOST = ''
TCP_PORT = 50021
BUFFER_SIZE = 1024
MESSAGE = "Hello Mate!"


print('Loading server public key...')
f = open('serverpublic.key', 'r')
keyfile = f.read()
serverpubkey = rsa.PublicKey.load_pkcs1(keyfile, 'PEM')
f.close()

if not os.path.isfile('public.key') or not os.path.isfile('private.key'):
   
   print("Gnerating RSA keys...")
   (pubkey, privkey) = rsa.newkeys(512)
   
   f = open('public.key', 'wb')
   f.write((pubkey.save_pkcs1('PEM')))
   f.close()
   
   f = open('private.key', 'wb')
   f.write((privkey.save_pkcs1('PEM')))
   f.close()
   
else:
   
   print("loading public key...")
   f = open('public.key', 'r')
   keyfile = f.read()
   pubkey = rsa.PublicKey.load_pkcs1(keyfile, 'PEM')
   f.close()
   #f.open('public.key','r')
   #pubkey = f.read()
   #f.close()
   
   print("loading private key...")
   f = open('private.key', 'r')
   keyfile = f.read()
   privkey = rsa.PrivateKey.load_pkcs1(keyfile,'PEM')
   f.close()
   #f.open('private.key', 'r')
   #privkey = f.read()
   #f.close()



print('Creating socket...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Socket connecting...')
s.connect((TCP_IP, TCP_PORT))



cryptmessage = rsa.encrypt(MESSAGE.encode(),serverpubkey)

print('Socket sent: ' + str(cryptmessage))
s.send(cryptmessage)


data = s.recv(BUFFER_SIZE)

decryptedData = rsa.decrypt(data,privkey)

print('Received Enrypted: ' + str(data))
print('Received Decrypted: ' + str(decryptedData))
s.close()

#print("Sent data:", data)