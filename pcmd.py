#!/usr/local/bin/python
# -*- coding: utf-8 -*- 
import getpass
import paramiko
import sys
#from debug import __print
import threading
import signal
import thread
import time

is_exit = False
s_result_data = {}
f_result_data = {}


def get_file_lines(fname):
    lines=[]
    f=open(fname)
    for line in f:
        line = line.strip()
        if(len(line)!=0):
          lines.append(line.split())
    return lines


def do_cmd(port,timeout,username,password,cmd):
    global is_exit,idx,mutex
    global iplist ,index
    ip = None
    while not is_exit:
        mutex.acquire()
        if(index>len(iplist)-1):
          is_exit = True
        else:
          ip=iplist[index]
          index=index+1
        mutex.release()
        if not is_exit and ip != None:
           try:
              ssh=paramiko.SSHClient()
              ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
              ssh.connect(hostname=ip,port=22,username=username,password=password,compress=True,timeout=10)
              stdin, stdout, stderr = ssh.exec_command(cmd)
              std = stdout.read()
              if(not s_result_data.has_key(ip)):
                 s_result_data[ip]=std
    
              ssh.close()
           except paramiko.ssh_exception.AuthenticationException:
                 f_result_data[ip]='密码验证失败'
           except paramiko.ssh_exception.SSHException:
                 f_result_data[ip]='未知错误1,如需获得更多信息.请尝试手动ssh连接该服务器.'
           except:
                 f_result_data[ip]='未知错误2,如需获得更多信息.请尝试手动ssh连接该服务器.'
    if is_exit:
        pass
    else:
        pass

def handler(signum, frame):
    global is_exit
    is_exit = True



if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    username = raw_input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    ip_file = str(sys.argv[1])
    cmd = str(sys.argv[2])
    global iplist ,index, mutex 
    port = 22
    timeout = 10
    index=0
    iplist=[]

    f=open(ip_file)
    for l in f:
        iplist.append(l.strip('\n'))

    cc = 20 
    threads = []
    mutex = threading.Lock()
    for i in range(cc):
        t = threading.Thread(target=do_cmd, args=(port,timeout,username,password,cmd))
        t.setDaemon(True)
        threads.append(t)
        t.start()
    while 1:
        alive = False
        for i in range(cc):
            alive = alive or threads[i].isAlive()
        if not alive:
            for ip in s_result_data:
                print ip
                print s_result_data[ip]
            for ip in f_result_data:
                print ip
                print f_result_data[ip]
            print "成功的数:"+str(len(s_result_data))
            print "失败的数:"+str(len(f_result_data))
            break
