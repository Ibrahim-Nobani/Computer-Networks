from socket import *
moviesArr=[]
#this method will read the movies in a file and put it in the moviesArr
def readMovies():
    file = open("Movies.txt", "r")
    fi = file.readlines()
    for line in fi:
        arr = line.split(",")
        arr[2] = (arr[2]).strip("\n")
        arr[1] = float(arr[1])
        arr[2] = float(arr[2])
        moviesArr.append(arr)
#a sort rating function to be a key in sorting
def SortRating(rating):
    return rating[1]
#a sort price function to be a key in sorting
def SortPrice(price):
    return price[2]
readMovies()#read the movies from a text file
#sendresponse function to send the response to the browser
def sendresponse (response):
    SocketConnect.send("\r\n".encode("UTF-8"))
    SocketConnect.send(response)
    SocketConnect.close()
#errorMessage function to send and display an error if the requested file is not found
def errorMessage(response):
    SocketConnect.send("HTTP/1.1 404 Not Found\r\n".encode("UTF-8"))
    SocketConnect.send("Content-Type: text/html \r\n".encode("UTF-8"))
    response = "<html><head><title>Error</title></head><body> <p style='color: red;'>THE FILE IS NOT FOUND </p><p><b>Ibrahim Nobani-1190278</b></p><p><b>Mahmoud Qaisi-1190831</b></p><p><b>Mohammed Adra-1180168</b></p><p>IP ADDRESS: " + \
               address[0] + "</p><p>PORT:" + str(
        address[1]) + "</p><img width='900' height='300' src='error.jpg' alt='ERROR'/></body> </html>"
    response = response.encode()
    sendresponse(response)
#sortResponse function to create an html file and return the response of sorting whether its a name sorting , price sorting or rate sorting
def sortResponse(response):
    response = '<!DOCTYPE html><html><link rel="stylesheet" type="text/css" href="./Sort.css"/><body><h2>Mini Movies Database</h2><table style='
    response += 'width:100%'
    response += '><tr><th>Movie Name</th><th>Movie Rating</th><th>Movie Price</th></tr>'
    for i in range(len(moviesArr)):
        response += '<tr>'
        for j in range(len(moviesArr[i])):
            response += '<td>' + str(moviesArr[i][j]) + '</td>'
        response += '</tr>'
    response += '</table></body></html>'
    return response
#Port at 6500
svrPort = 6500
Socket = socket(AF_INET, SOCK_STREAM)#create the socket
Socket.bind(("",svrPort))#bind it with the port number
Socket.listen(1)#listening and waiting for connection
print ("Connnection Established, Go to the local host server.")

while True:
    SocketConnect, address = Socket.accept()#accept connection and put the ip addressess and the port number in address
    request1h = SocketConnect.recv(1024).decode()#recieve the http request and put it in request1h
    print (request1h)
    requestedFile=""
    response=""
    tempRF=""
    if (request1h):
        requestedFile=request1h.split(' ', 2)[1]#take the requested file from the http request
        if '.' in requestedFile:
            tempRF = requestedFile[requestedFile.index('.'):]
    SocketConnect.send("HTTP/1.1 200 OK\r\n".encode("UTF-8"))

    try:
        if requestedFile == "/" :#by default, send the index file
            myfile = open("index.html", 'rb')#open the file
            response = myfile.read()#read the file

            SocketConnect.send("Content-Type: text/html \r\n".encode("UTF-8")) #send the type of the file
            sendresponse(response)#send the file to the sendresponse function
        elif tempRF == ".html":#if the requested file has an extension of html(the file is an html file)
            myfile = open(requestedFile.strip('/'), 'rb')#open the file
            response = myfile.read()#read the file

            SocketConnect.send("Content-Type: text/html \r\n".encode("UTF-8"))#send the type of the file
            sendresponse(response)#send the file to the sendresponse function
        elif tempRF == ".css":#if the requested file has an extension of css(the file is a css file)
            myfile = open(requestedFile.strip('/'), 'rb')#open the file
            response = myfile.read()#read the file

            SocketConnect.send("Content-Type: text/css \r\n".encode("UTF-8"))#send the type of the file
            sendresponse(response)#send the file to the sendresponse function

        elif tempRF == ".jpg":#if the requested file has an extension of jpg(the file is a jpg image)

            SocketConnect.send("Content-Type: image/jpeg \r\n".encode("UTF-8"))#send the type of the file
            myfile = open(requestedFile.strip('/'), 'rb')#open the file
            response = myfile.read()#read the file
            sendresponse(response)#send the file to the sendresponse function


        elif (tempRF == ".png"):#if the requested file has an extension of png(the file is a png image)

            SocketConnect.send("Content-Type: image/png \r\n".encode("UTF-8"))#send the type of the file
            myfile = open(requestedFile.strip('/'), 'rb')#open the file
            response = myfile.read()#read the file
            sendresponse(response)#send the file to the sendresponse function


        elif (requestedFile == "/SortName"):#if the request is /SortName,then sort the movies(based on their names),create an html file and send it
            SocketConnect.send("Content-Type: text/html \r\n".encode("UTF-8"))#send the type of the file
            moviesArr.sort()#sort the movies(based on movie`s name)
            response=sortResponse(response)#create an html file with the movies
            response = response.encode()#encode the file
            sendresponse(response)#send the file to the sendresponse function


        elif (requestedFile == "/SortPrice"):#if the request is /SortPrice,then sort the movies(based on their prices),create an html file and send it
            SocketConnect.send("Content-Type: text/html \r\n".encode("UTF-8"))#send the type of the file
            moviesArr.sort(reverse=True,key=SortPrice)#sort the movies(based on movie`s price) and list it in descending order)
            response=sortResponse(response)#create an html file with the movies
            response = response.encode()#encode the file
            sendresponse(response)#send the file to the sendresponse function
        elif (requestedFile == "/SortRating"):#if the request is /SortRating,then sort the movies(based on their ratings),create an html file and send it
            SocketConnect.send("Content-Type: text/html \r\n".encode("UTF-8"))#send the type of the file
            moviesArr.sort(reverse=True,key=SortRating)#sort the movies(based on movie`s rating) and list it in descending order)
            response = sortResponse(response)#create an html file with the movies
            response = response.encode()#encode the file
            sendresponse(response)#send the file to the sendresponse function
        else:#if its neither sorting type nor type of the file
            errorMessage(response)#send an error message
    except:#if an error occured
        errorMessage(response)#send an error message

