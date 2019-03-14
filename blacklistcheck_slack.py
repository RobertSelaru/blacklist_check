try:
    from rblwatch import RBLSearch
    import requests
    import os, sys, json
    import socket, ipaddress
    from prettytable import PrettyTable
except ImportError as e:
    msg = 'Module import error: {}'.format(e)
    exit(msg)


EXCEPTIONS = []
slack_url = os.environ.get('SLACK_WEB_URL')


try:
    arg = sys.argv[1]
except IndexError as e:
    msg = 'No argumets found. Please give either IP/HOSTNAME. A txt file is also supported'
    exit(msg)


def check_input_type(input):
    targets = list()
    output = list()

    if os.path.isfile(input):
        file = open(input, 'r').readlines()
        file = [line.rstrip('\n') for line in file]
        targets = file
    else:
        targets.append(input)
     
    for target in targets: 
        try:
            ips = set([r[4][0] for r in socket.getaddrinfo(target, None, 0, 1)])
            for ip in ips:
                output.append(ip)
        except socket.gaierror:
            msg = 'Skipping {}: Name or service not known'.format(target)
            print(msg)
    
    return output


def check_blacklist(ip):
    listed = []

    searcher = RBLSearch(ip)

    for blacklist, report in searcher.listed.items():
        if isinstance(report, dict) and report['LISTED'] == True:
            if blacklist not in EXCEPTIONS:
                listed.append(blacklist)

    return listed


def send_notification(msg):
    webhook_url = slack_url

    parms = {
        'Content-type': 'application/json',
    }

    slack_data = {
        'text': msg
    }

    response = requests.post(
        webhook_url, 
        data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )


def main():
    title = "*Blacklist*  (Robert Selaru) \n"
        
    targets = check_input_type(arg)
    rbl_data = list()

    for target in targets:
        rbl = check_blacklist(target)
        if rbl:
            rbl_data.append((target, rbl))

    x = PrettyTable()
    fielnames = ['Target', 'Blacklist(s)']
    x.field_names = fielnames

    for target, blacklists in rbl_data:
        rbl = ', '.join(str(x) for x in blacklists)
        x.add_row([target, rbl])


    for fielname in fielnames:
        x.align[fielname] = 'l'

    x = x.get_string()

    a = template + '```' + x + '```'
    send_notification(a)

if __name__ == '__main__':
    main()