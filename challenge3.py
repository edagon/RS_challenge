# Rackspace API Challenge 3
# Write a script that accepts a directory as an argument as well as a container 
# name. The script should upload the contents of the specified directory to the 
# container (or create it if it doesn't exist). The script should handle errors
# appropriately. (Check for invalid paths, etc.)

#!/usr/bin/python
import pyrax, os, sys, getopt
from time import sleep

pyrax.set_credential_file("credentials.txt")
cf = pyrax.cloudfiles

# -------------------------------------
# Testing the ARGs passed into script
# -------------------------------------

argv = sys.argv[1:]
path = ''
cname = ''
try:
   opts, args = getopt.getopt(argv,"hp:c:",["path=","cname="])
except getopt.GetoptError:
   print 'ERROR: use -h for proper usage'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print '<Usage>: challenge3.py -p <path> -c <container name>'
      sys.exit()
   elif opt in ("-p", "--path"):
      path = arg
   elif opt in ("-c", "--cname"):
      cname = arg

if len(argv) in range(3):
   if path == '':
      print 'Error: Missing Path'
   if cname == '':
      print 'Error: Missing Container Name'
   sys.exit()  
else:
   print 'path >', path
   print 'container name >', cname

# -------------------------------------
# Test for Valid Path
# -------------------------------------
if os.path.isdir(path):
   print path,"is valid"
else:
   print "Path Error:  Invalid Path"
   sys.exit()
  
# -------------------------------------
# Passing Directory (path) to Container
# > If container does not exist, then
# > upload_folder will create it   
# -------------------------------------

upload_key, total_bytes = cf.upload_folder(path,container = cname)

print 'Container is building'
while (pyrax.cloudfiles.get_uploaded(upload_key)-total_bytes) != 0:
   sleep(1)
   print 'Bytes uploaded >',pyrax.cloudfiles.get_uploaded(upload_key)
print 'Upload Complete'
print '='*40
for container in cf.get_all_containers():
   if container.name == cname:
       print 'Container stats:'
       print 'Name:', container.name
       print '# of objects:', container.object_count
       print 'Total Bytes:',container.total_bytes

