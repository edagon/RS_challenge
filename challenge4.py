# Rackspace API Challenge 4
# Write a script that uses Cloud DNS to create a new A record when 
# passed a FQDN and IP address as arguments.

#!/usr/bin/python
import pyrax, os, sys, getopt
from time import sleep

pyrax.set_credential_file("credentials.txt")
dns = pyrax.cloud_dns

# -------------------------------------
# Definition Section
#     >  VerifiedIP(<str>) - Boolean
#     >  DomainExists(<str>) - Boolean
#     >  print_domains() 
# -------------------------------------
def VerifiedIP(ip):
    ip_= ip.split('.')
    if len(ip_) != 4:
      print 'ERROR: Invalid IP address'
      return False
    else:
      
      for octet in ip_:
        try:
          if int(octet) not in range(0,255):
             print "ERROR: An Octet is out of range"
             return False
        except ValueError:
             print "ERROR: Invalid IP address"
             return False
    return True

def DomainExists(domain):
    domains = dns.get_domain_iterator()
    inlist = False 
    for dom in domains:
        if dom.name == domain:
           inlist = True
           break
    if not inlist:
       print 'ERROR: Domain [',domain,'] does not exist.'
    return inlist

def print_domains():
    print '-'*30
    print '  Current Domains  '
    print '-'*30
    for domain in dns.get_domain_iterator():
      print domain.name
    print '-'*30

# -------------------------------------
# Testing the ARGs passed into script
# -------------------------------------

argv = sys.argv[1:]
ip = ''
domain = ''
print_domains()
try:
   opts, args = getopt.getopt(argv,"hi:f:",["help","ip=","domain="])
except getopt.GetoptError:
   print 'ERROR: use -h for proper usage'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print '='*40
      print '<Usage>: challenge4.py -f <FQDN> -i <ip>'
      print '='*40
      sys.exit()
   elif opt in ("-i", "--ip"):
      ip = arg.strip()
      
   elif opt in ("-f", "--FQDN"):
      domain = arg

if len(opts) != 2:
     print 'ERROR: use -h for proper usage'
else:
    if not VerifiedIP(ip):
       sys.exit()
    elif not DomainExists(domain):
       sys.exit()
    else:
       print domain,' exists'
       print 'A record is being created'
       type = "A"
       ttl = 6000
       try:
          dom = dns.find(name=domain)
          rec = dom.add_records({"type": type, "name": domain,
                   "data": ip, "ttl": ttl}) 
       except pyrax.exceptions.DomainRecordAdditionFailed:
          print "ERROR:  An error occurred trying to create the record" 
       else:
          print 'Record Created'
          print '-'*50 
          print rec       
