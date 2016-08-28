import socket
import rsa

SEND_PORT = 50021

print("Gnerating RSA keys...")
(pubkey, privkey) = rsa.newkeys(512)

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

    print("The data was: ")
    print(data)

    if data:
        client.send(data)

    client.close()


print("Clsoing socket...")
s.close()
