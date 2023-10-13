import paramiko

ip = '127.0.0.1'
username = 'root'
password = 'root'
port = 22

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

class SSHCommand:
    
    def vizov(self, cmd: str):
        stdin, stdout, stderr = ssh.exec_command(cmd)
        for i in stdout.readlines(): 
            print(i)
        
    def main(self):

        ssh.connect(hostname=ip, username=username, password=password, port=23)
        #clear HYSTORY
        self.vizov("unset HISTFILE && rm -f /root/.ash_history")
        
        #CHECK
        self.vizov("date")
        self.vizov("uname -a")
        self.vizov("id")
        self.vizov("cat /etc/issue") #хрень
        self.vizov("ifconfig")
        
        #clear HYSTORY
        self.vizov("unset HISTFILE && rm -f /root/.ash_history")
        
        ssh.close()

if __name__ == '__main__':
    parser = SSHCommand()
    parser.main()