import socket
import rsa
import os.path

SEND_PORT = 50021

if not os.path.isfile('public.key') or not os.path.isfile('private.key'):
   
   print("Gnerating RSA keys...")
   (pubkey, privkey) = rsa.newkeys(512)
   
   f = open('public.key', 'w')
   f.write(pubkey.save_pkcs1('PEM'))
   f.close()
   
   f = open('private.key', 'w')
   f.write(privkey.save_pkcs1('PEM'))
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
   

print("loading client public key...")
f = open('clientpublic.key', 'r')
keyfile = f.read()
clientpubkey = rsa.PublicKey.load_pkcs1(keyfile, 'PEM')
f.close()

message = 'hello mate!'
cryptmessage = rsa.encrypt(message,pubkey)

print("Encrypted message: " + cryptmessage)
print("Decrypted message: " + rsa.decrypt(cryptmessage, privkey))

print("Signing message...")
signature = rsa.sign(message, privkey, 'SHA-1')

print("verifying message...")
print("Message verrified = " + str(rsa.verify(message, signature, pubkey)))

print("Creating socket...")
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("Binding socket...")
s.bind(('',SEND_PORT))

#s.settimeout(0.1)

print("Port listening...")
s.listen(5)

while 1:
    print("Socket accepting...")
    client, addr = s.accept()
    print ('connected with ' + addr[0] + ':' + str(addr[1]))

    print("Recieving data...")
    data = client.recv(1024)
   
    print("Enrypted data: " + str(data))
    decryptedData = rsa.decrypt(data,privkey)
    print("Decrypted data: " + str(decryptedData))
    
    MESSAGE = "I received your data"
    
    encryptedData = rsa.encrypt(MESSAGE.encode(), clientpubkey)

    client.send(encryptedData)

    client.close()


print("Clsoing socket...")
s.close()
