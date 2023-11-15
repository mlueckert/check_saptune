#!/usr/bin/env python3
# coding=utf-8
################################################
# Author: Marc Lückert
# Version: 0.1
# Purpose: Checks the output of "saptune status"
# Requirements: User must have root or sudo permission to run "saptune status"
#################################################

import subprocess
import sys
import re

def function_exit(status):
    if status == "OK":
        sys.exit(0)
    if status == "WARNING":
        sys.exit(1)
    if status == "CRITICAL":
        sys.exit(2)
    if status == "UNKNOWN":
        sys.exit(3)

def get_worst_status(status_list):
    if "CRITICAL" in status_list:
        return "CRITICAL"
    if "WARNING" in status_list:
        return "WARNING"
    if "UNKNOWN" in status_list:
        return "UNKNOWN"
    return "OK"

def check_sudo(check_string):
    compare_string = r".*(root|password|Administrator).*"
    if re.match(compare_string, check_string, re.IGNORECASE|re.DOTALL):
        status = 'WARNING'
        print(f'{status} - "saptune status" cannot be run, the user is missing sudo permissions to run it.')
        function_exit(status)

def check_saptune_output(check_string):
    check_string = check_string.replace("\n","&&")
    regex_string = r"saptune\.service: *(?P<saptune_service>.*?)&&.*(configured|applied) Solution: *(?P<configured_solution>.*?)[&&| (].*system state: *(?P<system_state>.*?)&&.*"
    status = ["OK"]
    output_list = []
    matches = re.search(regex_string, check_string, re.IGNORECASE|re.MULTILINE)
    if not matches:
        output_list += "Output of saptune status did not match the search criteria. Check the plugin."

    saptune_service = matches.group('saptune_service')
    if "enabled/active" not in saptune_service:
            output_list.append(f"saptune.service!=\"enabled/active\" (current value {saptune_service})")
            status.append("CRITICAL")
    else:
        output_list.append(f"saptune.service=\"{saptune_service}\"")
    
    configured_solution = matches.group('configured_solution')
    if not configured_solution:
            output_list.append(f"configured Solution=EMPTY (no solution configured)")
            status.append("CRITICAL")
    else:
        output_list.append(f"configured Solution=\"{configured_solution}\"")

    system_state = matches.group('system_state')
    if "running" not in system_state:
            output_list.append(f"system state!=\"running\" (current value \"{system_state}\")")
            status.append("CRITICAL")
    else:
        output_list.append(f"system state=\"{system_state}\"")

    if( get_worst_status(status) in ["WARNING","CRITICAL"]):
        output_list.insert(0, "Output of saptune status reports issues.")


    print(f"{get_worst_status(status)} - {' // '.join(output_list)}")
    function_exit(get_worst_status(status))

if __name__ == '__main__':
    try:
        # We try to run saptune status with sudo and return the output as text
        arguments = ['sudo','-n','/usr/sbin/saptune','status']
        process = subprocess.run(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        check_sudo(process.stderr)
        check_saptune_output(process.stdout)

    except Exception as e:
        print("WARNING: An error occured: {0}".format(repr(e)))
        function_exit('WARNING')