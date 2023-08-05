# cozypy

Cozytouch python implementation

This API allows you to control Atlantic, Thermor and Sauter equipment via the Cozytouch bridge

Used to obtain information from the following sensors:
  - Gateway
  - Radiators
  - Water heaters and other counters

### Example

     from cozytouchpy import CozytouchClient
     
     username="my-username"
     password="my-password"
     
     client = CozytouchClient(username, password)
     setup = await client.async_get_setup() 
     for place in setup.places:  
         print(place.id)


