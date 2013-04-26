# Rackspace API Challenge 8
# Write a script that will create a static webpage served out of Cloud Files. The script 
# must create a new container, cdn enable it, enable it to serve an index file, create an 
# index file object, upload the object to the container, and create a CNAME record pointing 
# to the CDN URL of the container.

#!/usr/bin/python
import pyrax, os, sys, getopt
from time import sleep

pyrax.set_credential_file("credentials.txt")
cf = pyrax.cloudfiles
dns = pyrax.cloud_dns
content = '3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113'

#  ============================================================
#  Definition Section
#
#  print_records(cont) - prints CONTAINER information
#  ValidHost(name) - determines the validit of DOMAIN and HOST
#  ============================================================

def print_record(cont):
   print "="*30
   print "[cdn_enabled]:", cont.cdn_enabled
   print "[cdn_ttl]:", cont.cdn_ttl
   print "[cdn_log_retention]:", cont.cdn_log_retention
   print "="*30

def ValidHost(name):
   name_ = name.split('.')

   if len(name_) != 3:
      print 'ERROR1: Domain not correct format'
      print '   use: host.domain.com'
      sys.exit()
   else:
      i = 0
      while i < len(name_):
         if len(name_[i]) == 0:
            print 'ERROR2: Improper Name'
            print '   use: host.domain.com'
            sys.exit()
         i += 1
   name2 = name_[1]+'.'+name_[2]
   print name2,' --> domain name'
   domainfound = False 
   for domain in dns.get_domain_iterator():
       if domain.name == name2:
          domainfound = True
          domain_ = domain
      
   if domainfound:
        print 'domain,',domain_.name,',accepted!'
        for sub in list(dns.get_record_iterator(domain_)):
            subfound = False
            if sub.name == name:
                subfound = True
                print 'host,',name_[0],', already created'
                print 'Please create a different HOST'
                sys.exit()
        if not subfound:
           print 'host,',name_[0],', accepted!'
           return domain_
   else:
        print 'domain,',name,', does not exist!'
        print 'Please create the domain and try again!'
        sys.exit()

# -------------------------------------
# Testing the ARGs passed into script
# -------------------------------------

argv = sys.argv[1:]
cont = ''
count = 0
try:
   opts, args = getopt.getopt(argv,"hc:n:",["help","cont=","name="])
except getopt.GetoptError:
   print 'ERROR: use -h for proper usage'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print '='*41
      print '<Usage>: challenge8.py -c <container name> -n <hostname>'
      print ' '*6,'| <hostname> = host.domain.com'
      print '='*41
      sys.exit()
   elif opt in ("-c", "--container"):
      cont = arg
      count += 1
   elif opt in ("-n", "--hostname"):
      name = arg
      count += 1
if count in (0,1):
   print 'ERROR: use -h for proper usage'
   sys.exit()  

if len(argv) != 4:
   print 'ERROR: use -h for proper usage'
   sys.exit()
else:
   print 'container name = ',cont

# test if hostname already exists

dom = ValidHost(name)

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

# Copying CONTENT to Object | Creating index.html
# Attaching URL information 

obj = cf.store_object(cont, "index.html", content)
print 'Stored Object:', obj

objurl =cont.cdn_uri+ '/index.html'
objurl = objurl[7:]

# create domain > name

rec = [{
        "type": "CNAME",
        "name": name,
        "data": objurl,
        "ttl": 600,
        }]

print dns.add_records(dom,rec)

