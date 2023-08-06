# -*- coding: utf-8 -*-
import os
from flask import Flask, request
import json
import logging
import datetime
import logging
import logdna
from logdna import LogDNAHandler
import fcntl, socket, struct
import click

__version__ = '0.0.1'

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret')

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

if not os.environ.get('LOGDNA_AGENT_KEY', None):
    print(" * LOGDNA_AGENT_KEY variable is not set. Logs will not be sent to logging platform.")
    logdna_agent_key = False
else:
    logdna_agent_key = os.environ.get('LOGDNA_AGENT_KEY')
if not os.environ.get('LOGDNA_URL', None):
    print(f" * LOGDNA_URL       variable is not set.   Using default: `{logdna.configs.defaults.get('LOGDNA_URL')}' to send to endpoint")
else:
    logdna.configs.defaults['LOGDNA_URL'] = os.environ.get('LOGDNA_URL')
if not os.environ.get('OUTPUT_FILE', None):
    print(" * OUTPUT_FILE      variable is not set.   Using default: `output.txt' to write payloads to disk")
    output_file = "output.txt"
else:
    output_file = os.environ.get('OUTPUT_FILE')

print(" * fyi              this app is logging everything sent to /_webhook\n"
      f"                    EXAMPLE:\n                            curl -X POST -d 'hello_world' http://{socket.gethostbyname(socket.gethostname())}:5000/_webhook/testing/webhooks")

if logdna_agent_key:
    log = logging.getLogger('logdna')
    log.setLevel(logging.DEBUG)

    options = {
      'app': 'answerbook_webhook_test',
      'ip': socket.gethostbyname(socket.gethostname())
    }

    # who cares if we don't have an eth0 interface
    try:
        options['hwaddr'] = getHwAddr('eth0')
    except:
        pass

    # Defaults to False; when True meta objects are searchable
    options['index_meta'] = True

    logdnahandler = LogDNAHandler(logdna_agent_key, options)
    log.addHandler(logdnahandler)
    log.info("Logging class init")

@app.route('/')
def hello():
    content = {
        "app": "answerbook_webhook_test",
        "tagline": "You know, for the webhook tests..."
        }
    return json.dumps(content, indent=3)

@app.route("/_webhook/<path:path>", methods=['GET', 'POST'])
def catch_all(path):
    if request.method != 'POST':
        return 'It works! But this resource only supports POST'
    r = 77
    r1 = 12
    url = str(request.url)
    date = str(datetime.datetime.now())
    data = str(request.get_data().decode("utf-8") )
    lines_text = ("*"*r+"\n"+date+" - "+url+"\n"+data+"\n")
    lines_platformlog = (url+"\n"+"*"*r1+"    POST PAYLOAD BELOW    "+"*"*r1+"\n"+data)
    print(lines_text)
    with open(output_file, "a") as output:
        output.write(lines_text)
    print(lines_text)
    if logdna_agent_key:
        log.warn(lines_platformlog, {'meta': {'url': url, 'route': str(request.url_rule)}})
    return lines_text


@click.command()
def cli():
    app.run(host=os.environ.get('LISTEN_HOST', '0.0.0.0'), port=os.environ.get('LISTEN_PORT', 80))
