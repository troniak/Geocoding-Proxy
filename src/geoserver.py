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

    print request

    conn = httplib.HTTPSConnection('maps.googleapis.com',timeout=10)
    conn.request('GET','/maps/api/geocode/json?address='+request+'&key='+mapsAPI)
    http_response = conn.getresponse();
    success = http_response.status == 200

    if not success:
        conn = httplib.HTTPSConnection('geocoder.cit.api.here.com')
        conn.request('GET','/6.2/geocode.json?app_id='+hereAppID+'&app_code='+hereAppCode+'&searchtext='+request)
        http_response = conn.getresponse();

    success = http_response.status == 200

    if not success:
        client_response = error_message;
    else:
      client_response = http_response.read(1024);

    client_connection.sendall(client_response)
    client_connection.close()
