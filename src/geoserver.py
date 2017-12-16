from config import mapsAPI,hereAppCode,hereAppID,error_message

import socket
import httplib
import re

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
    conn.request('GET','/maps/api/geocode/json?address='+request+'&key='+mapsAPI)
    http_response = conn.getresponse();
    latre = '(?<="lat" : )-?[0-9]+\.?[0-9]*';
    lngre = '(?<="lng" : )-?[0-9]+\.?[0-9]*';
    success = http_response.status == 200

    if not success:
      url = 'geocoder.cit.api.here.com'
      get = '/6.2/geocode.json?app_id='+hereAppID+'&app_code='+hereAppCode+'&searchtext='+request
      conn = httplib.HTTPConnection(url)
      conn.request('GET',get)
      http_response = conn.getresponse();
      latre = '(?<="Latitude":)-?[0-9]+\.?[0-9]*'
      lngre = '(?<="Longitude":)-?[0-9]+\.?[0-9]*'

    success = http_response.status == 200

    if not success:
      client_response = error_message;
    else:
      http_response_text = http_response.read();
      latmatch = re.search(latre,http_response_text)
      latstr = latmatch.group(0);
      lngmatch = re.search(lngre,http_response_text)
      lngstr = lngmatch.group(0);

      client_response = "("+latstr+","+lngstr+")";

    client_connection.sendall(client_response)
    client_connection.close()
