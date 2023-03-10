from socket import *
import time


target_port = 80  # the port we want to connect to which is the port used for internet purposes
client = socket(AF_INET, SOCK_STREAM)  # create a TCP clint
target_host = input("Enter The wanted URL:")  # the URL entered by the user
try:  # this to handle the error in case the user enters a false URL Address.
    client.connect((target_host, target_port))
    # Here the socket will connect to the given URL through port 80 as provided
    for i in range(0, 3):
        # the cline will send the request multiple times through the same connection because its of type TCP.
        request = "HEAD / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
        # the format of the HTTP request. Notice how HEAD t the begining means we want the head of the age only.
        start = time.time()  # Take the time before the Request is sent.
        client.send(request.encode())
        response = client.recv(4096)
        roundtrip = time.time() - start  # Take the time before the Request is sent to calculate the elapsed Time
        SimlifiedRTT = "{:.2f}".format(roundtrip * pow(10, 3))
        # only to format the time so it can be more understandable.
        print("*********HTTP Response:******")
        print(response)
        print("*********Elapsed Time:*******")
        print(SimlifiedRTT + "ms")
except gaierror: # gai error is a short for get adder which appears when there is a problem connecting to the URL
    print("Incorrect URL or URL doesn't exist")
