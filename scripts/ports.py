#!/usr/bin/env python3

import sys, datetime, os, configargparse, socket

parser = configargparse.ArgParser()
#parser.add_argument("nmap_files", type=argparse.FileType('r'), nargs='*', help="files to parse for ports")
parser.add_argument("nmap_files", nargs='+', help="files to parse for ports")
parser.add_argument("--r", "-r", env_var='resolve_hosts', action="store_true", help="resolve hostnames")
args = parser.parse_args()

print(args.nmap_files)

#open(file)
#print("opening %s" % file)

cwd = os.getcwd()

for nmap_file in args.nmap_files:
   nmap_file = str(nmap_file)
   with open(nmap_file, 'r') as f:
      for line in f:
         if '/open/' in line:
            fields = line.split()
             
            d = 'ports'
            if not os.path.exists(d):
                    os.makedirs(d)
            
            for service in range(1, 65535):
            #for service in services:
               if " " + str(service) + "/open/tcp" in line:
                  if args.r:
                     try: 
                        host = socket.gethostbyaddr(fields[1])
                     except socket.error:
                        host = fields[1] 
                  else:
                     host = fields[1]

                  try:
                     port = socket.getservbyport(service)
                     print(str(port), host)
                  except socket.error:
                     port = service
                     print(str(port), host)
                  f = open("ports/port." + str(port), 'a')
                  f.write(fields[1] + "\n")
 
                  if args.r:
                     ip_dns = open("ports/port-hostname." + str(port), 'a')
                     ip_dns.write(str(host) + ":" + fields[1] + "\n")
