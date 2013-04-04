# Rackspace API Challenge 2
# Write a script that clones a server (takes an image and deploys 
# the image as a new server).

# USAGE - challenge2.py can be run as-is from the command line.  
#       - credentials.txt is the file that needs to be adjusted for validation

import pyrax
from time import sleep
pyrax.set_credential_file("credentials.txt")

# -----------------------------------------
# Def'n Section:
#    (1) print_server
# -----------------------------------------

def print_server(server,pwd):
        print "="*70
        print "Server >",server.name,"[",server.status,"]"
        print "="*70
        print "Admin password:", pwd
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

print len(cs.servers.list()),"servers exist!"

if len(cs.servers.list()) == 0:   # if there aren't any servers, stop
   print "ERROR:  There are NO servers to COPY"  
   print "Please create a server first"
else:
# -----------------------------------------
#  Create Copy (Saved Images)
#  It becomes the 0th member of the cs.images.list()
# -----------------------------------------
   for server in cs.servers.list():
      print "-",server.name
   for server in cs.servers.list():
      if server.status == "ACTIVE":
           server1 = cs.servers.get(server.id)
           server1.create_image("CH1_COPY")
           print "[CLONED] Server is being copied from",server.name
           break
   servername = server.name

   images = cs.images.list()
   for image in images:
     if image.name in "CH1_COPY":
        image_= image

   print image_.name," is being created."
   print image_.name,"|",image_.status

# -----------------------------------------
#  Waiting for IMAGE to become ACTIVE so that
#  the cloning can occur
# -----------------------------------------
   while image_.status <> "ACTIVE":
       sleep(20)
       image_ = cs.images.get(image_.id)
       print image_.name,"|",image_.status

# -----------------------------------------
#  Choose the FLAVOR (512MB in this case)
# -----------------------------------------
   flavors = cs.flavors.list()
   flave = [flavor for flavor in flavors
           if flavor.ram == 512][0]
   print "Using", flave,"MB for this server's usage"

# -----------------------------------------
#  Create the clone server
#  with image.id and flavor
# -----------------------------------------
   server = cs.servers.create("CH2_WEB0",image_.id,flave)
   pwd = server.adminPass
   print "Cloning Image to New Server | CH2_WEB0"

# -----------------------------------------
#  Waiting for the server to be created
# -----------------------------------------
   while server.status <> "ACTIVE":
       sleep(20)
       server = cs.servers.get(server.id)
       print server.name,"|",server.status

   print_server(server,pwd)
