#!/usr/bin/env python3
import os
import time
import psutil
import argparse

parser = argparse.ArgumentParser(description='Get some stats.')
parser.add_argument('--cpu', '-c', help='Check CPU parameters',         action='store_true')
parser.add_argument('--gpu', '-g', help='Check GPU parameters',         action='store_true')
parser.add_argument('--ram', '-r', help='Check RAM paramters',          action='store_true')
parser.add_argument('--down','-d', help='Check download speed',         action='store_true')
parser.add_argument('--up',  '-u', help='Check upload speed',           action='store_true')
parser.add_argument('--ping','-p', help='Check download speed',         action='store_true')
parser.add_argument('--net', '-n', help='Check all network parameters', action='store_true')
parser.add_argument('--all', '-a', help='Check all possible parameters',action='store_true')
args = parser.parse_args() 

import sys
def loading(str,y=None):
    if y == None:
        y = 20
    else:
        x = y
        y = x 
    for i in range(0,y):
        b = f'{str}'+'.'*i
        print(b,end='\r')
        time.sleep(0.1)
    sys.stdout.write("\033[K")

def cpu():
    loading('Checking CPU Usage', 10)
    print(f'CPU usage: {psutil.cpu_percent(interval=None)}%')
    percpu = psutil.cpu_percent(interval=None, percpu=True)
    print(f'Usage by Threads: {psutil.cpu_count()}')
    for i in range(len(percpu)):
        print(i+1, ' - ', f'[{percpu[i]}%]')
    
def gpu():
    from gpuinfo import GPUInfo
    try: 
        percent,memory = GPUInfo.gpu_usage()
        if len(memory) >= 1:
            loading('Checking GPU Usage',8)
        else: loading('Checking GPUs Usage',10)
        print('VRAM:') 
        for i in range(len(memory)):
            print(i+1, ' - ', f'[{memory[i]}]MB Used') 
        print('CPU Usage:','\n', percent)
        
    except:
        print('Only Nvidia GPUs are compatible.')

def ram():
    loading('Checking RAM Usage', 10)
    print(f'RAM usage: {psutil.virtual_memory().percent}%')
    free = round(psutil.virtual_memory().available*100/psutil.virtual_memory().total ,1)
    print(f'Available: {free}%')


import speedtest
st = speedtest.Speedtest()
def down():
    loading('Checking Download Speed')
    print(round(st.download()/1000000, 3), 'ups')

def up():
    loading('Checking Upload Speed')
    print(round(st.upload()/1000000,3), 'downs')

def ping():
    loading('Tesing Ping')
    servers=[]
    st.get_servers(servers)
    print(st.results.ping, 'ms')

def net():
    os.system('speedtest-cli')

def run_all():
    cpu()
    gpu()
    ram()
    net()

def main():
    if args.cpu:
        cpu()
    elif args.gpu:
        gpu()
    elif args.ram:
        ram()
    elif args.down:
        down()
    elif args.up:
        up()
    elif args.ping:
        ping()
    elif args.net:
        net()
    elif args.all:
        run_all()

if __name__ == '__main__':
    main()
