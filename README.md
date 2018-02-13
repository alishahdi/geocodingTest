# Geocoding Test Readme

The code implements a local HTTP server on port 8888 with REST APIs for retreiving latitude and longitiude of a given address. The address has to be included in the path.

Run the code to start the http server and in your browser send a GET request to the HTTP server with the address in the path e.g. *http://localhost:8888/ADDRESS*

* GET /ADDRESS/

Returns the JSON in the following format

	{
   	 	"status": "OK", "Invalid", "Disconnected" 
   	 	"Lat": "Latitude"
		"Lng": "Longitude"
		"source": "Google", "HERE"
	}


The code will try to use Google APIs first to retreive the lat/lng for the address. If the address is invalid (or no address is in the path) it will return *Invalid* as the status. If it fails to connect to Google servers it will then try to use HERE APIs to retreive the lat/lng. In the JSON output file the source of the lat/lng is returned in the *source* field. In case both Google and HERE APIs are failing (e.g. in the case of no connection) the JSON response will have the status of *Disconnected*.

Please note other REST APIs (POST, DELETE, PUT, and DELETE) are not implemented.
