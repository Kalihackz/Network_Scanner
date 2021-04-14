import urllib3
import time
from termcolor import cprint
import os,subprocess,threading,getmac
import texttable as tt

ips = []
macs = []
vendors = []

url = "http://macvendors.co/api/vendorname/"

class IP:

    def __init__(self):
        cprint('''  _   _      _       _____                                 
 | \ | |    | |     / ____|                                
 |  \| | ___| |_   | (___   ___ __ _ _ __  _ __   ___ _ __ 
 | . ` |/ _ \ __|   \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | |\  |  __/ |_    ____) | (_| (_| | | | | | | |  __/ |   
 |_| \_|\___|\__|  |_____/ \___\__,_|_| |_|_| |_|\___|_|  \n''','green')
        cprint("                               - A Network Scanner for all\n","magenta")
        cprint("                                           Version : Final\n","red") 
        cprint("                                              By Kalihackz\n","cyan") 
        cprint("\nStarting the Network Scanner ...","yellow")

    @staticmethod
    def pingIp(ip):
        global ips
        try:
            output = subprocess.check_output(f"ping -n -c 1 -w 5 {ip}", shell=True)
            if "0% packet" in str(output):
                cprint(ip+" up","green")
                ips.append(ip)
        except:
            pass
    
    def scanNetwork(self,subnet,host_ip):
        cprint("[+] Scanning LAN for online devices ...\n","green")
        for i in range(1,255):
            ip = subnet+"."+str(i)
            if ip != host_ip:
                t = threading.Thread(target=self.pingIp,args=(ip,))
                t.start()

    def findMacAddressAndVendor(self,ipList):
        global macs,vendors
        for ip in ipList:
            mac = getmac.get_mac_address(ip=ip)
            if mac != None:
                http = urllib3.PoolManager()
                r = http.request('GET',url + mac, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.2171.95 Safari/537.36'})
                vendor_name = r.data.decode('utf-8')
                vendors.append(vendor_name)
                macs.append(mac)

def main():
    try:
        scanner = IP()
        cprint("[+] Enter subnet [For Example : 192.168.1] : ","green",end="")
        subnet = input()
        cprint("[+] Enter your IP : [For example : 192.168.1.x] : ","green",end="")
        host_ip = input()
        scanner.scanNetwork(subnet,host_ip)
        time.sleep(5)
        cprint("All other devices are down\n","red")
        scanner.findMacAddressAndVendor(ips)
        cprint("\n[+] Preparing table . . . \n\nIP-MAC-VENDOR table",'green')
        cprint("*Current Host IP will not be shown in the table",'yellow')
        time.sleep(2)
        tab = tt.Texttable()
        headings = ['IP Address', 'Mac Address' , 'Vendor Name']
        tab.header(headings)
        for row in zip(ips,macs,vendors):
                tab.add_row(row)
        s = tab.draw()
        cprint(s,"cyan")
        cprint("\n[+] Exiting ...\n","red")
    except KeyboardInterrupt:
        cprint("\n\n[-] Forced Exiting ...\n","red")

if __name__ == "__main__":
    main()
