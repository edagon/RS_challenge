# Rackspace API Challenge 6
# Write a script that creates a CDN-enabled container in Cloud Files.

#!/usr/bin/python
import pyrax, os, sys, getopt
from time import sleep

pyrax.set_credential_file("credentials.txt")
cf = pyrax.cloudfiles

# -----------------------------------------
# Def'n Section:
#    (1) print_record (container)
# -----------------------------------------

def print_record(cont):
   print "="*30
   print "[cdn_enabled]:", cont.cdn_enabled
   print "[cdn_ttl]:", cont.cdn_ttl
   print "[cdn_log_retention]:", cont.cdn_log_retention
   print "="*30

# -------------------------------------
# Testing the ARGs passed into script
# -------------------------------------

argv = sys.argv[1:]
cont = ''                     # Container Name
count = 0
try:
   opts, args = getopt.getopt(argv,"hc:",["help","cont="])
except getopt.GetoptError:
   print 'ERROR: use -h for proper usage'
   sys.exit(2)
for opt, arg in opts:
   print opt,arg
   if opt == '-h':
      print '='*41
      print '<Usage>: challenge6.py -c <container name>'
      print '='*41
      sys.exit()
   elif opt in ("-c", "--container"):
      cont = arg
      count += 1
if count == 0:
   print 'ERROR: use -h for proper usage'
   sys.exit()  

if len(argv) != 2:
   print 'ERROR: use -h for proper usage'
   sys.exit()
else:
   print 'container name = ',cont

#  Creat a Container with name > cont

   cont = cf.create_container(cont)
   print '='*45
   print 'Container [',cont.name,']: Created'
   print '='*45
   print_record(cont)

# Enable the container, cont.name

   print '='*45
   print 'Container [',cont.name,']: CDN ENABLED'
   print '='*45
   cf.make_container_public(cont.name, ttl=900)
   print_record(cont)
