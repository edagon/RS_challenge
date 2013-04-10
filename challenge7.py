# Rackspace API Challenge 7
# Write a script that will create 2 Cloud Servers and add 
# them as nodes to a new Cloud Load Balancer.

#!/usr/bin/python
import pyrax, os, sys, getopt
from time import sleep

pyrax.set_credential_file("credentials.txt")
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers
servers = cs.servers.list()
lbs = clb.list()

# -----------------------------------------
# Def'n Section:
#    (1) print_lbinfo(loadbalancer)
#    (2) ConfirmedServers(srv1,srv2)
#    (3) CreateServers(srv1,srv2)
# -----------------------------------------

def print_lbinfo(lb):
   print "*"*31
   print "   Load Balancer Information"
   print "*"*31
   print "Load Balancer:", lb.name
   print "           ID:", lb.id
   print "       Status:", lb.status
   i = 0
   for node in lb.nodes:
      i += 1
      n0d3 = str(node).strip('<').strip('>').split(',')
      print '        Node',i,':'
      for elem in n0d3:
         print '               ',elem
   print "  Virtual IPs:"
   for info in lb.virtual_ips:
       vip = str(info).strip('<').strip('>').split(',')
       for elem in vip:
         print '               ',elem
   print "    Algorithm:", lb.algorithm
   print "     Protocol:", lb.protocol
   print "*"*31

def ConfirmedServers(srv1,srv2):
   srv1_ = True
   srv2_ = True
   for server in servers:
      if server.name == srv1:
        srv1_ = False
        print 'Server [',server.name,'] already exists.'
      if server.name == srv2:
        srv2_ = False
        print 'Server [',server.name,'] already exists.'
   exists = srv1_ and srv2_
   return exists

def CreateServers(srvr1,srvr2):
   img_id = "5cebb13a-f783-4f8c-8058-c4182c724ccd"
   flavor_id = 2

   server1 = cs.servers.create(srvr1, img_id, flavor_id)
   s1_id = server1.id
   server2 = cs.servers.create(srvr2, img_id, flavor_id)
   s2_id = server2.id

# -----------------------------------------------
# The servers won't have their networks assigned 
# immediately, so wait until they do.
# -----------------------------------------------

   while not ((server1.status and server2.status) in 'ACTIVE'):
       sleep(20)
       server1 = cs.servers.get(s1_id)
       server2 = cs.servers.get(s2_id)
       print '> [',server1.name,'|',server1.status,'] and [',
       print server2.name,'|',server2.status,']'
       print '> [',server1.name,'|',server1.status,'] and [',
       print server2.name,'|',server2.status,']'

# -------------------------------------
# Testing the ARGs passed into script
# -------------------------------------

argv = sys.argv[1:]
srv1 = ''
srv2 = ''
lb = ''

print '='*30
print ' Current Servers '
print '='*30
for server in servers:
  print server.name
print '='*30

try:
   opts, args = getopt.getopt(argv,"hn:m:l:",["help","srv1=","srv2=","lb="])
except getopt.GetoptError:
   print 'ERROR: use -h for proper usage'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print '='*30
      print '<Usage>: challenge7.py -m <server1> -n <server2>',
      print '-l <load balancer>'
      print '='*30
      sys.exit()
   elif opt in ("-m", "--server1"):
      srv1 = arg.strip()
   elif opt in ("-n", "--server2"):
      srv2 = arg
   elif opt in ("-l", "--loadbalancer"):
      lb = arg

if len(opts) != 3:
  print 'ERROR: Number of Arguments not accepted'
  print 'use -h option for usage'
  sys.exit()
else:
  if ConfirmedServers(srv1,srv2):
     print 'Server Names do not exist - [PASS]'
     print 'Please Wait while servers build ...'
     CreateServers(srv1,srv2)
  else:
     print 'ERROR:  One or Two of the Servers already exist...'
     print '     >  Please use different names '
     sys.exit()

print '='*30
print ' Current Load Balancers '
print '='*30
continue_ = True
if len(lbs) == 0:
  print 'No Load Balancers exist'
else:
  for lbal in lbs:
    print lbal.name
    if lb == lbal.name:
        continue_ = False
print '='*30
if not continue_:
   print 'Loadbalancer [',lb,'] already exists'
   print '   >  Please use different name'
   sys.exit()
else:
   print 'Loadbalancer does not exist - [PASS]'

# ------------------------------------
# Create the Nodes
# ------------------------------------

servers = cs.servers.list()
list = servers[:2]

node1 = clb.Node(address=list[0].networks["private"][0], 
                 port=80, condition="ENABLED")
node2 = clb.Node(address=list[1].networks["private"][0], 
                 port=80, condition="ENABLED")

# Create the Virtual IP for the Load Balancer
vip = clb.VirtualIP(type="PUBLIC")

# ------------------------------------
# Create the Loadbalancer with 2 nodes
# ------------------------------------

list = servers[:2]
lb_ = clb.create(lb, port=80, protocol="HTTP",
        nodes=[node1,node2], virtual_ips=[vip])

print_lbinfo(lb_)
 
