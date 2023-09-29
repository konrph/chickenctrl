import os
import glob
import time

def search_services():
    results=[]
    for service in glob.glob('/etc/systemd/system/*'):
        servicename = service.split('/')[-1]
        if servicename.startswith('chicken'):
            results.append(servicename)

    return results



def restart_services(services):
    print('start stopping services')
    for service in services:
        status = os.system('systemctl stop '+str(service))





def main():
    restart_services(services=search_services())


if __name__ == '__main__':
    main()


