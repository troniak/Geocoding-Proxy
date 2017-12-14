from config import mapsAPI,hereAppCode,hereAppID,error_message

import socket
import httplib

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)

    conn = httplib.HTTPSConnection('maps.googleapis.com')
    conn.request('GET','/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key='+mapsAPI)
    http_response = conn.getresponse().read()

    success = 0;

    if not success:
        conn = httplib.HTTPSConnection('geocoder.cit.api.here.com')
        conn.request('GET','/6.2/geocode.json?app_id='+hereAppID+'&app_code='+hereAppCode+'&searchtext=425+W+Randolph+Chicago')
        http_response = conn.getresponse().read();

    success = 1;

    if not success:
        http_response = error_message;

    client_connection.sendall(http_response)
    client_connection.close()
