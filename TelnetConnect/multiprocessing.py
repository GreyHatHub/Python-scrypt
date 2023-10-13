import xtelnet
import multiprocessing
import random
import time

#-------- Setting ---------
ip1 = '192.168.1.100' #just an example
use1 = 'admin'
pas1 = 'admin'
port1 = 23

ip2 = '192.168.1.101' #just an example
use2 = 'admin'
pas2 = 'admin'
port2 = 23

ip3 = '192.168.1.102' #just an example
use3 = 'admin'
pas3 = 'admin'
port3 = 23

ip4 = '192.168.1.103' #just an example
use4 = 'admin'
pas4 = 'admin'
port4 = 23

# Initial
term1 = xtelnet.session()
term2 = xtelnet.session()
term3 = xtelnet.session()
term4 = xtelnet.session()

class INIT:
    
    def one(self, lineup,f):       
        IoT1.connect(ip1, username=use1, password=pas1, p=port1, timeout=5)
        output1 = IoT1.execute('cli enable')
        output1 = IoT1.execute('enable on')
        output1 = IoT1.execute('power off')
        exp=0
        while exp <= 4:
            exp=1
			# else code

    def two(self, lineup,f):       
        IoT2.connect(ip2, username=use2, password=pas2, p=port2, timeout=5)
        output1 = IoT2.execute('cli enable')
        output1 = IoT2.execute('enable on')
        output1 = IoT2.execute('power off')             
        exp=0
        while exp <= 4:
            exp=1
			# else code
                
                
    def three(self, lineup,f):       
        IoT3.connect(ip3, username=use3, password=pas3, p=port3, timeout=5)
        output1 = IoT3.execute('cli enable')
        output1 = IoT3.execute('enable on')
        output1 = IoT3.execute('power off')             
        exp=0
        while exp <= 4:
            exp=1
			# else code			
    

    def four(self, lineup,f):       
        term4.connect(ip4, username=use4, password=pas4, p=port4, timeout=5)
        output1 = IoT4.execute('cli enable')
        output1 = IoT4.execute('enable on')
        output1 = IoT4.execute('power off')             
        exp=0
        while exp <= 4:
            exp=1
			# else code

    
    def run (self):
        p1 = multiprocessing.Process(target = self.one, args = [20, 2])
        time.sleep(0.01)
        p2 = multiprocessing.Process(target = self.two, args = [20, 2])
        time.sleep(0.01)
        p3 = multiprocessing.Process(target = self.tree, args = [20, 2])
        time.sleep(0.01)
        p4 = multiprocessing.Process(target = self.four, args = [20, 2])
          
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        
        p1.join()
        p2.join()        
        p3.join()     
        p4.join()
        
        
    def off(self):
        term1.connect(ip1, username=use1, password=pas1, p=port1, timeout=5)
        output1 = term1.execute('pn off')
        term2.connect(ip2, username=use2, password=pas2, p=port2, timeout=5)
        output1 = term2.execute('pn off')
        term3.connect(ip3, username=use3, password=pas3, p=port3, timeout=5)
        output1 = term3.execute('pn off')
        term4.connect(ip4, username=use4, password=pas4, p=port4, timeout=5)
        output1 = term4.execute('pn off')
        
        
    def main (self):
        print("\n[0. Stop work ]")
        print("[1. Start work ]")
       
        countvpn=input("\n[Enter number setting]: ")
        if countvpn.__len__()==0:
            print('\nEXIT')
        elif countvpn=='0':
            self.off()          
        elif countvpn=='1':
            self.run()
        
        
 #-----------START-----------        
if __name__ == '__main__':
    parser = INIT()
    parser.main()
