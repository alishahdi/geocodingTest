# Ali Shahdi
# Coding test

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2
import json

# Class for handling REST APIs
class RESTHandler(BaseHTTPRequestHandler): 
	# Generating the header for HTTP response
	def _set_headers(self): 
		self.send_response(200)
        	self.send_header('Content-type', 'text/html')
	        self.end_headers()

	# Respond to GET requests
        def do_GET(self): 		
		# Ignore faivcon requests
		if self.path == '/favicon.ico': 
			pass
		else:
			# Generate the header
		        self._set_headers() 
			# Send geocoding requests using Google and HERE APIs and parse the lat/lng results for the address	
			jsonOutput = self.geoCode() 
			# Send back the result to the requester
		        self.wfile.write(jsonOutput)
	
	# Not doing anything on REST POST requests
	def POST(self):
		pass

    	# Geocoding the address
        def geoCode(self): 
		# Get the address from the requester URL path	
		address = self.path 

		# Try using Google APIs first (failure to connect be simulated by changing this URL)
		try: 
			# Google geocoding API GET request
			geoURL = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyDzVSbsHjzNyN6LEcASEJ29Cmrj9ET4qZo" % address 
			request = urllib2.urlopen(geoURL)
			jsonResponse = json.loads(request.read())
		
			# If the returned staus is OK parse lat/lng and return the values
			if jsonResponse['status'] == 'OK': 
   				plat = jsonResponse['results'][0]['geometry']['location']['lat']
   				plng = jsonResponse['results'][0]['geometry']['location']['lng']

				# Creating the JSON output from the lat/lng info
				data = {}
				data['status'] = 'OK'
				data['lat'] = plat
				data['lng'] = plng
				data['source'] = 'Google'
				jsonOutput = json.dumps(data)
				return jsonOutput
			# Google servers responded but the address was invalid
			else:
				data = {}
				data['status'] = 'Invalid'
				data['source'] = 'Google'
				jsonOutput = json.dumps(data)
				return jsonOutput
	
		# Google servers cannot be reaced, trying to use HERE APIs as the backup (catching all the exceptions)	
		except:
			try:
				print("Google failed trying HERE")
				
				#HERE geocoding API GET request
				geoURL = "https://geocoder.cit.api.here.com/6.2/geocode.json?app_id=ykrI6wAjdahtpMwgZxhh&app_code=t1R7EyxS-G_q-VT78OcikA&searchtext=%s" % address 

				request = urllib2.urlopen(geoURL)
				jsonResponse = json.loads(request.read())
			
				# Check to see if the result is valid and return the values
				if len(jsonResponse['Response']['View']) > 0: 
	
		   			plat = jsonResponse['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude']
		   			plng = jsonResponse['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']
					
					# Creating the JSON output from the lat/lng info
					data = {}
					data['status'] = 'OK'
					data['lat'] = plat
					data['lng'] = plng
					data['source'] = 'HERE'
					jsonOutput = json.dumps(data)
					return jsonOutput
				else:
					# HERE servers has responded but the address was invalid
					data = {}
					data['status'] = 'Invalid'
					data['source'] = 'HERE'
					jsonOutput = json.dumps(data)
					return jsonOutput
			
			# HERE APIs are also failing
			except: 
				return "All servers down. Please try again!"
			
# Running the HTTP server on PORT 8888        
def runServer(serverClass = HTTPServer, handlerClass = RESTHandler, port = 8888): 
   	address = ('', port)
	httpServer = serverClass(address, handlerClass)
	print 'Starting the http server on port %d ...' % port
	try:
	        httpServer.serve_forever()
	except KeyboardInterrupt:
		pass
	print 'Stopping the HTTP server ...'
	http_server.server_close()


# __main__
if __name__ == "__main__":
        runServer()
