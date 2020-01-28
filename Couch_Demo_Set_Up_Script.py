import requests
import json
import sys

db_names = ["devices", "device_type", "rooms", "buildings", "room_configurations"]
devices_documents = ["pi3", "sonyXBR", "HDMI1", "HDMI2", "HDMI3"]
rooms_documents = ["room"]
device_type_documents = ["pi3", "sonyXBR", "HDMI"]
buildings_documents = ["buildings"]
room_configurations_documents = ["default"]

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
        status = addDBDocument("device_type",device_type_data[x])
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

    headers = {
        #If you have added authorization the following header is required. it is admin:{yourpassword} base64 encoded
        'Authorization': "Basic YWRtaW46QllVQ09VR0FSUw==",
        }

    response = requests.request("PUT", url, headers=headers)
    return response.status_code


# Add a new document to a DB
def addDBDocument(dbname, document):
    import requests

    url = "http://localhost:5984/{}/{}".format(dbname, document["_id"])
    print(url)
    payload = json.dumps(document)
    headers = {
        'Content-Type': "application/json",
        #If you have added authorization the following header is required. it is admin:{yourpassword} base64 encoded
        'Authorization': "Basic YWRtaW46QllVQ09VR0FSUw==",
        }

    response = requests.request("PUT", url, data=payload, headers=headers)

    return response.status_code

# Run the setup Script
setUpScript()


