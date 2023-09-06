# Description

Just a small python script that runs "saptune status" and parses the output of it.  
Can be used in Nagios compatible environments, I use it with OMD.

## Requirements

- To run "saptune status" the user requires root or sudo permissions.

## Output example

CRITICAL - Output of saptune status reports issues. // saptune.service!="enabled/active" (current value disabled/inactive) // configured Solution=EMPTY (no solution configured) // system state!="running" (current value "degraded")

OK - saptune.service="enabled/active" // configured Solution="S4HANA-DBSERVER" // system state="running"
