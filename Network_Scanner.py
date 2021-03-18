import urllib3
import scapy.all as scapy
import sys,time
from termcolor import cprint
import os,subprocess,threading,getmac
import texttable as tt

ips = []
macs = []
vendors = []

url = "http://macvendors.co/api/vendorname/"

def scan_ip(ip):
    try:
        output = subprocess.check_output(f"ping -n -c 1 -w 5 {ip}", shell=True)
        if "0% packet" in str(output):
            cprint(ip+" up","green")
            ARP_table(ip)
    except:
        pass

def ping_hosts():
    cprint('''\n███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝     ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗     ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝\n''','green')
    cprint("Enter subnet xxx.xxx.xxx [For Example : 192.168.1]: ","yellow" ,end='')
    subnet = input()

    cprint("[+] Scanning LAN for online devices ...\n","green")
    for i in range(1,255):
        ip = subnet+"."+str(i)
        t = threading.Thread(target=scan_ip,args=(ip,))
        t.start()

def ARP_table(ip):
    try: 
        mac = getmac.get_mac_address(ip=ip)
        http = urllib3.PoolManager()
        r = http.request('GET',url + mac, headers={'User-Agent': "API Browser"})
        vendor_name = r.data.decode('utf-8')
        vendors.append(vendor_name)
        macs.append(mac) #list to string
        ips.append(ip)
    except Exception as e:
        pass

def main():
    ping_hosts()
    time.sleep(5)
    cprint("All other devices are down","red")
    tab = tt.Texttable()
    headings = ['IP Address', 'Mac Address' , 'Vendor Name']
    tab.header(headings)
    for row in zip(ips,macs,vendors):
            tab.add_row(row)
    s = tab.draw()
    cprint("\n[+] Preparing table . . . \n\nIP-MAC-VENDOR table",'green')
    cprint("*Current Host IP is not shown in the table",'yellow')
    print(s)

if __name__ == "__main__":
    main()
