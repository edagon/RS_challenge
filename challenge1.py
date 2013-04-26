# Rackspace API Challenge 1
# Write a script that builds three 512 MB Cloud Servers that following 
# a similar naming convention. (ie., web1, web2, web3)and returns the 
# IP and login credentials for each server. Use any image you want. 

# USAGE - challenge1.py can be run as-is from the command line.  
#       - credentials.txt is the file that needs to be adjusted for validation

import pyrax
from time import sleep
pyrax.set_credential_file("credentials.txt")

# -----------------------------------------
# Def'n Section:
#    (1) print_server
# -----------------------------------------
def print_server (server):
        print "="*70
        print "Server >",server.name,"[",server.status,"]"
        print "="*70
        print "Admin password:", server.adminPass
        pubkey = u'public'
        prikey = u'private'
        if len(server.networks[pubkey][0]) > 18:        
              print "  (IPv4)   Public IP:", server.networks[pubkey][1],
              print "     Private IP:", server.networks[prikey][0]
              print "  (IPv6)   IP:", server.networks[pubkey][0]
        else: 
              print "  (IPv4)   Public IP:", server.networks[pubkey][0],
              print "     Private IP:", server.networks[prikey][0]
              print "  (IPv6)   IP:", server.networks[pubkey][1]
# -----------------------------------------
# Get Server information from API
# -----------------------------------------

cs = pyrax.cloudservers

# -----------------------------------------
# Print Current Server Listing
# -----------------------------------------
print "-"*40
print "Current Server Listing"
print "-"*40
if len(cs.list()) <> 0:
     for servers in cs.list():
       print "server> ",servers
else:
     print "0 servers currently exist"
print "-"*40

# -----------------------------------------
# Select Image and Flavor of Servers
#      image = Fedora 16
#      flavor = 512MB 
# -----------------------------------------
images = cs.images.list()
image = [img for img in images
  if "Ubuntu 12.04" in img.name][0]
print "Image Selected ", image

flavors = cs.flavors.list()
flave = [flavor for flavor in flavors
	if flavor.ram == 512][0]
print "RAM | ", flave

# -----------------------------------------
# Creating Servers 
# 3 servers with standard naming Convention
#	>  CH1_WEB
# -----------------------------------------
name = 'CH1_WEB'
servers = {}
for i in range(3):
    name_ = name + str(i)
    servers[name_] = cs.servers.create(name_, image, flave)
    print servers[name_].name,"is being built (please wait)"
print "Building >"

# -----------------------------------------
# List Servers/Status along with:
#    > Password
#    > IPs
# -----------------------------------------
completed = []
while len(completed) < 3:
     sleep(10)
     for name, server in servers.iteritems():
         if name in completed:
            continue
         server.get()
         if server.status in ['ACTIVE', 'ERROR', 'UNKNOWN']:
             if server.status <> 'ACTIVE':
               print "Error Building",server.name
               print "Delete the entry and re-create"
               comleted.append(name)
             else:
               print_server(server)
               completed.append(name)

