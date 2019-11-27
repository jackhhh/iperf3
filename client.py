#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import socket
import subprocess
import sys
import time
import urllib2

env_dict = os.environ

cmd_run = 'iperf3 -f m -c '

api_url = 'http://172.16.69.134:8081/v2/demo_data/load_data'

if __name__ == '__main__':

    pm_id = env_dict.get('pm_id')
    vm_id = env_dict.get('vm_id')
    app_id = socket.gethostname()
    server_ip = sys.argv[1]

    while True:
        ret_run = subprocess.Popen(cmd_run + server_ip, shell=True, stdout=subprocess.PIPE, close_fds=True).communicate()

        line_bandwidth_send = ret_run[0].split('\n')[-5].split()
        line_bandwidth_recv = ret_run[0].split('\n')[-4].split()
        bandwidth_send = int(line_bandwidth_send[line_bandwidth_send.index('Mbits/sec') - 1])
        bandwidth_recv = int(line_bandwidth_recv[line_bandwidth_recv.index('Mbits/sec') - 1])
        
        json_array = []

        json_obj_send = json.loads('{}')
        json_obj_send['pm_id'] = pm_id
        json_obj_send['vm_id'] = vm_id
        json_obj_send['app_id'] = app_id
        json_obj_send['metric_type'] = 2
        json_obj_send['timestamp'] = int(time.time())

        json_obj_send['key'] = 'iperf_bandwidth_send'
        json_obj_send['value'] = bandwidth_send
        json_array.append(json_obj_send)

        json_obj_recv = json.loads('{}')
        json_obj_recv['pm_id'] = pm_id
        json_obj_recv['vm_id'] = vm_id
        json_obj_recv['app_id'] = app_id
        json_obj_recv['metric_type'] = 2
        json_obj_recv['timestamp'] = int(time.time())

        json_obj_recv['key'] = 'iperf_bandwidth_recv'
        json_obj_recv['value'] = bandwidth_recv
        json_array.append(json_obj_recv)

        print json_array

        headers = {'Content-Type': 'application/json'}
        postdata = json.dumps(json_array)
        request = urllib2.Request(api_url, data=postdata, headers=headers)
        try:
            f = urllib2.urlopen(request, timeout=2)
            response = f.read()
            f.close()
            print response
        except Exception as ex:
            print ex

