# RBL (blacklist) check 
Python scripts for checking whether IP or HOSTNAME is blacklisted.

### blacklist_crew
This version is used on a crew-server can be simply called with ip or hostname as argument.

Example:
```
λ flaysx@flaysx-pc [dev/blacklist-check] at  master ✔ 
→ py blacklistcheck_crew.py 192.168.11.1                                                                                                                                                                                       [3809ce4]
192.168.11.1 is blacklisted on bogons.cymru.com

λ flaysx@flaysx-pc [dev/blacklist-check] at  master ✔ 
→ py blacklistcheck_crew.py sol7.nl                                                                                                                                                                                            [3809ce4]
sol7.nl is not blacklisted
```

### blacklist_slack
This version will send a slack notification using a slack_web_url and expects `SLACK_WEB_URL` variable to be set.
Add the followiung line to your bash / zsh profile to export the `SLACK_WEB_URL`:
```
export SLACK_WEB_URL="https://hooks.slack.com/services/your_service_id
```

This script is running as cron and supports txt list of ips or hostnames as input.

Example:
```
λ flaysx@flaysx-pc [dev/blacklist-check] at  master ✔ 
→ cat ~/list                                                                                                                                                                                                                   [3809ce4]
192.168.11.1
sol7.nl
justawronghostname
1000.1.1.1

λ flaysx@flaysx-pc [dev/blacklist-check] at  master ✔ 
→ py blacklistcheck_slack.py ~/list                                                                                                                                                                                            [3809ce4]
Skipping justawronghostname: Name or service not known
Skipping 1000.1.1.1: Name or service not known
```

Slack notification:
```
SysAdmin BOT APP [12:19 PM]
*RBL check* `https://github.com/RobertSelaru/blacklist_check`
+--------------+-------------+------------------+
| IP address   | Reverse DNS | Blacklist(s)     |
+--------------+-------------+------------------+
| 192.168.11.1 | None        | bogons.cymru.com |
+--------------+-------------+------------------+
```

### blacklist_zabbix
This version is used in zabbix as external_script and returns 1 if listed, 0 if not listd, 2 if argument is invallid

Example:
```
λ flaysx@flaysx-pc [dev/robert_pcx/blacklist-check] at  master ✔ 
→ py blacklistcheck_zabbix.py 192.168.1.1                                                                                                                                                                                      [3809ce4]
1

λ flaysx@flaysx-pc [dev/robert_pcx/blacklist-check] at  master ✔ 
→ py blacklistcheck_zabbix.py sol7.nl                                                                                                                                                                                          [3809ce4]
0

λ flaysx@flaysx-pc [dev/robert_pcx/blacklist-check] at  master ✔ 
→ py blacklistcheck_zabbix.py qwer123                                                                                                                                                                                          [3809ce4]
2
```