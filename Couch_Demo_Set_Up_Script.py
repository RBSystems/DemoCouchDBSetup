import requests
import json
import sys
import base64
import wget

# The raw json files required for the DB
devicesUrl = "https://raw.githubusercontent.com/byuoitav/DemoCouchDBSetup/master/devices.json"
roomsUrl = "https://raw.githubusercontent.com/byuoitav/DemoCouchDBSetup/master/rooms.json"
deviceTypesUrl = "https://raw.githubusercontent.com/byuoitav/DemoCouchDBSetup/master/device_type.json"
buildingsUrl = "https://raw.githubusercontent.com/byuoitav/DemoCouchDBSetup/master/buildings.json"
roomConfigurationUrl = "https://raw.githubusercontent.com/byuoitav/DemoCouchDBSetup/master/room_configurations.json"

# used for loading up the DB
db_names = ["devices", "device_types", "rooms", "buildings", "room_configurations"]
devices_documents = ["pi3", "sonyXBR", "HDMI1", "HDMI2", "HDMI3"]
rooms_documents = ["room"]
device_type_documents = ["pi3", "sonyXBR", "HDMI"]
buildings_documents = ["buildings"]
room_configurations_documents = ["default"]

# Check to see if the files are already downloaded, if they aren't download them using the URL's above
try:
    f = open("devices.json")
except:
    f = wget.download(devicesUrl)
try:
    f = open("rooms.json")
except:
    f = wget.download(roomsUrl)
try:
    f = open("device_type.json")
except:
    f = wget.download(deviceTypesUrl)
try:
    f = open("buildings.json")
except:
    f = wget.download(buildingsUrl)
try:
    f = open("room_configurations.json")
except:
    f = wget.download(roomConfigurationUrl)

# Open the files and load the JSON
with open('devices.json') as json_file:
    devices_data = json.load(json_file)
with open('rooms.json') as json_file:
    rooms_data = json.load(json_file)
with open('device_type.json') as json_file:
    device_type_data = json.load(json_file)
with open('buildings.json') as json_file:
    buildings_data = json.load(json_file)
with open('room_configurations.json') as json_file:
    room_configurations_data = json.load(json_file)

message = str(sys.argv[1]) + ":" + str(sys.argv[2])
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic "+base64_message,
        }

def setUpScript():
    # Check DB connection
    DBConnected = checkDBConnection()
    if DBConnected is not True:
        print("CouchDB is not running on 5986.")
        sys.exit(1)
    
    # Create required DB's for AV API
    for db in db_names:
        status = createDB(db)
        if status != 201:
            print("failed to create {} database".format(db))
            sys.exit(1)
    
    # Fill the DB with the required documents
    for x in devices_documents:
        status = addDBDocument("devices",devices_data[x])
        if status != 201:
            print("failed to add {} to database".format(x))
            sys.exit(1)

    for x in rooms_documents:
        status = addDBDocument("rooms",rooms_data[x])
        if status != 201:
            print("failed to add {} to database".format(x))
            sys.exit(1)

    for x in device_type_documents:
        status = addDBDocument("device_types",device_type_data[x])
        if status != 201:
            print("failed to add {} to database".format(x))
            sys.exit(1)

    for x in buildings_documents:
        status = addDBDocument("buildings",buildings_data[x])
        if status != 201:
            print("failed to add {} to database".format(x))
            sys.exit(1)

    for x in room_configurations_documents:
        status = addDBDocument("room_configurations",room_configurations_data[x])
        if status != 201:
            print("failed to add {} to database".format(x))
            sys.exit(1)


    print("Complete! Your DB is all set up and ready to go for the demo.")
    
    
# Check to make sure that the DB is up and running
def checkDBConnection():
    print('Checking if CouchDb is running on port 5984')
    url = "http://localhost:5984/"

    response = requests.request("GET", url)

    if response.text:
        print("CouchDB is running.")
        return True
    else:
        return False

# Create a new DB
def createDB(dbName):
    url = "http://localhost:5984/{}".format(dbName)

    response = requests.request("PUT", url, headers=headers)
    return response.status_code


# Add a new document to a DB
def addDBDocument(dbname, document):
    import requests

    url = "http://localhost:5984/{}/{}".format(dbname, document["_id"])
    payload = json.dumps(document)

    response = requests.request("PUT", url, data=payload, headers=headers)

    return response.status_code

# Run the setup Script
setUpScript()


