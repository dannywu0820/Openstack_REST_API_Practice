import requests
import json

home_url = "http://192.168.23.130"
nova_port = "8774"
glance_port = "9292"
identity_port = "5000"
neutron_port = "9696"

token_url = home_url+":"+identity_port+"/v3/auth/tokens"
body = {
    "auth":{
        "identity":{
            "methods":[
                "password"
            ],
            "password":{
                "user":{
                    "name":"admin",
                    "domain":{
                        "name":"Default"
                    },
                    "password":"admin"
                }
            }
        },
        "scope":{
            "project":{
                "name": "admin",
                "domain":{
                    "name":"Default"
                }
            }
        }
    }
}

#get token from keystone
response = requests.post(token_url, json = body)
head = response.headers.items()

X_Auth_Token = ""
#Token looks like this: "gAAAAABYOrsmRJweuWSXD7oJ8BbI7FR51cNdAcEjPjaOtrBXC26UmuSESYhfeRsLw9IvuIzz2DbYOtzkCCHvN9MsdWp8JDMFY0cbPXbu3tAgIVl9CmPX208lNrnJQtELhV3tsZoOhNkQ242mqeDlZW_9xrQrnjsp_KJZbh7Yy891hiY9VcN5NJk"
for item in head: #each item is a tuple
    if item[0] == 'X-Subject-Token':
        X_Auth_Token = item[1]
print X_Auth_Token


flavor_url = home_url+":"+nova_port+"/v2/flavors"
print flavor_url
image_url = home_url+":"+glance_port+"/v2/images"
print image_url
server_url = home_url+":"+nova_port+"/v2.1/servers"
print server_url
headers = {"Content-Type":"application/json", "X-Auth-Token": X_Auth_Token}

#get image id from glance
response = requests.get(image_url, headers = headers)
response_body = response.json()

print "image list"
images = response_body["images"]
image_id = ""
for image in images:
    if image["name"] == "cirros-0.3.4-x86_64-uec":
        image_id = image["id"]
print image_id

#get flavor id from nova
response = requests.get(flavor_url, headers = headers)
response_body = response.json()

print "flavor list"
flavors = response_body["flavors"]
flavor_id = ""
for flavor in flavors:
    if flavor["name"] == "m1.nano":
        flavor_id = flavor["id"]
print flavor_id

#create server(launch instance)
instance_name = "myInstance"
body = {
    "server":{
        "name": instance_name,
        "imageRef": image_id,
        "flavorRef": flavor_url+"/"+flavor_id,
        "networks":[
            {
                #found from horizon->networks->one of the networks called public
                "uuid":"2060f0a9-d525-4c77-ba38-dec3d337eac6"
            }
        ]
    }
}

response = requests.post(server_url, headers = headers, json = body)
print response.json()