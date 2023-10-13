import whois
import socket
import dns.resolver
from progress.bar import IncrementalBar
# =============================================================================
def BlackList(dnss):
    result=-1
    bList={'.local', 'gvt1.com', 'gvt2.com', '.gov', '.mil','office','microsoft','googl','amazon', 'cloudflare', 'cloudfront', 'kaspersky', 'kas-labs', 'bing' ,'addr.arpa', 'ip6.arpa', 'adobe', 'msn.com', 'akamai', 'msftncsi', 'mcafee.com', 'trafficmanager.com', 'yahoo.com', 'youtube', 'akadns', 'apple', 'aliyuncs', 'facebook', 'tiktok', 'instagram', 'twitter', 'doubleclick', 'xiaomi', 'fbcdn.net', 'sophos', 'footprint', 'eset', ' '}
    for i in bList:
        if dnss.find(i)!=-1: return 0
    return result
# =============================================================================

# =============================================================================
def DNSseach(dnss):
    try:
        w=whois.whois(dnss)
        if 'registrant_name' in w.keys():
            file.write(str(f'###########################################\r\n DNS = {dnss} - {w["registrant_name"]}\r\n###########################################\r\n'))
        elif 'domain_name' in w.keys():
            file.write(str(f'###########################################\r\n DNS = {dnss}\r\n###########################################\r\n'))
            file.write(str(w['domain_name'])+'\r\n')
        else:
            file.write(str(f'N/A \r\n {w}\r\n'))
        
        try:
            file.write(str(socket.gethostbyname(dnss)+'\r\n'))
        except:
            file.write(str('Local network\r\n'))
        
        for qtype in 'CNAME', 'A', 'AAAA', 'MX', 'NS', 'TXT', 'PTR':
            try: 
                answer = dns.resolver.resolve(dnss,qtype)
                if answer.rrset is not None:
                    file.write(str(answer.rrset))
            except:
                {}
        file.write('\r\n')
    except:
        file.write(str(f'###########################################\r\n DNS = {dnss} - error\r\n###########################################\r\n'))
# =============================================================================
    
#./CrawlerDNS/TEXT.txt
file = open("DNS-FILE", "w")            
print('    !!!RUN ONLY _PYTHON_v3_!!!    ')
filename=input("[Enter filename with DNS list]: ")

# =============================================================================
try:
    handle = open("./"+filename, "r")
    ListDNS=set(handle.read().split('\n'))
    bar = IncrementalBar('Download', max = len(ListDNS))
    
    for i in ListDNS:
        if BlackList(i)==-1 and len(i)>4:
            DNSseach(str(i))
        bar.next()
        
    print('\r\nCompl')
    handle.close()
    file.close()
    bar.finish()
except:
    print('\r\nFile Not Found - Error')
