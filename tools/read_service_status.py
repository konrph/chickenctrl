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


def printer(text,color=None):
    if color =='green':
        print('\033[32m'+str(text)+'\033[0m')
    elif color == 'red':
        print('\033[31m'+str(text)+'\033[0m')
    elif color == None:
        print(str(text))

def check_services(services):
    printer(text='start checking services',color=None)
    for service in services:
        status = os.system('systemctl is-active --quiet '+str(service))
        if status == 0:
            printer(text=str(service)+'  running',color='green')
        else:
            printer(text=str(service) + '  stopped', color='red')




def main():
    check_services(services=search_services())
    time.sleep(1)
    check_services(services=search_services())
    time.sleep(1)
    check_services(services=search_services())

if __name__ == '__main__':
    main()


