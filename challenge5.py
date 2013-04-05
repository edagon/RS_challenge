# Rackspace API Challenge 5
# Write a script that creates a Cloud Database instance. This instance 
# should contain at least one database, and the database should have at 
# least one user that can connect to it. 


#!/usr/bin/python
import pyrax, os, sys, getopt
from time import sleep

pyrax.set_credential_file("credentials.txt")
cdb = pyrax.cloud_databases

# -------------------------------------
# Testing the ARGs passed into script
# -------------------------------------

argv = sys.argv[1:]
instance = ''
db = ''
user = ''

try:
   opts, args = getopt.getopt(argv,"hi:d:u:",["help","inst=","db=","user="])
except getopt.GetoptError:
   print 'ERROR: use -h for proper usage'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print '='*75
      print '<Usage>: challenge5.py -i <instance name> -d <database name>',
      print '-u <user name>'
      print '='*75
      sys.exit()
   elif opt in ("-i", "--instance"):
      instance = arg.strip()
   elif opt in ("-d", "--db"):
      db = arg
   elif opt in ("-u", "--user"):
      user = arg

if len(opts) != 3:
  print 'ERROR: Number of Arguments not accepted'
  print 'use -h option for usage'
else:

# creating instance (-i instance)

  inst = cdb.create(instance,flavor="1GB Instance", volume=2)
  print 'The instance,',instance,',is being created. Please wait for it to complete.'
  
  while inst.status != 'ACTIVE':
     inst = cdb.get(inst)
     print instance,'|',inst.status
     sleep(15)
  print '='*55
  print 'The instance,',instance,', has completed and is ACTIVE.'
  print 'For this challenge, default settings are:' 
  print '       RAM = 1GB'
  print '    Volume = 2GB'
  print '-'*30
  
# creating database (-d database)

  dbase = cdb.create_database(inst,db)
  print 'The database,',db,', has been created.'
  print '-'*30

# creating user (-u user)

  pwd = '#Osd34fs@_sd1f$%'
  user_ = inst.create_user(name=user, password=pwd, database_names=[dbase])
  print "User:", user,
  print "Password:",pwd
  print '='*55
