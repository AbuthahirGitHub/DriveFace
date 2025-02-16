from flask import Flask, send_file, render_template_string
import qrcode
import socket
import netifaces
import os
from werkzeug.serving import run_simple

app = Flask(__name__)

# Get local IP address
def get_local_ip():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface != 'lo':
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    return addr['addr']
    return '127.0.0.1'

# Create QR code
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save('test_qr.png')

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>DriveFace Test Server</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            .container { text-align: center; }
            .qr-code { margin: 20px; }
            .instructions { margin: 20px; text-align: left; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DriveFace Test Server</h1>
            <div class="qr-code">
                <img src="/qr" alt="QR Code">
            </div>
            <div class="instructions">
                <h2>Test Instructions:</h2>
                <ol>
                    <li>Scan the QR code with your DriveFace app</li>
                    <li>The app should connect to this test server</li>
                    <li>Test results will appear below</li>
                </ol>
                <h3>Server Status: Running</h3>
                <p>Server IP: {{ip}}</p>
                <p>Port: {{port}}</p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, ip=get_local_ip(), port=5000)

@app.route('/qr')
def serve_qr():
    server_url = f"http://{get_local_ip()}:5000"
    generate_qr(server_url)
    return send_file('test_qr.png', mimetype='image/png')

@app.route('/test')
def test():
    return {
        'status': 'success',
        'message': 'Test server is running correctly'
    }

if __name__ == '__main__':
    ip = get_local_ip()
    print(f"Starting test server at http://{ip}:5000")
    print("Scan the QR code in your browser to test the app")
    run_simple(ip, 5000, app, use_reloader=True) 