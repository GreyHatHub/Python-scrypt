import whois #pip install python-whois
import socket
import dns.resolver
from progress.bar import IncrementalBar

# =============================================================================
def DNSseach(dnss):
     try:
         addr = socket.gethostbyname(dnss)
         file.write('"'+dnss+'"'+'\t'+addr+'\r\n')
     except:
         file.write(str(f'{dnss}\tLocal\r\n'))

# =============================================================================
    
# ./CrawlerDNS/DNS.txt
file = open("DNS-IP-OUT", "w")            
print('    !!!RUN ONLY _PYTHON_v3_!!!    ')
filename=input("[Enter filename with DNS list]: ")

# =============================================================================

try:
     handle = open("./"+filename, "r")
     ListDNS=set(handle.read().split('\n'))  
     
     bar = IncrementalBar('Download', max = len(ListDNS))
     for i in ListDNS:
         DNSseach(str(i))
         bar.next()
         
     print('\r\nCompl')
     handle.close()
     file.close()
     bar.finish()
except:
     print('\r\nFile Not Found - Error')
# =============================================================================