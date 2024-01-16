try:
    import usocket as socket
except:
    import socket

import network
from machine import Pin

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MicroPython-AP'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)

while ap.active() == False:
    pass

print('Connection successful')
print(ap.ifconfig())

led_pin = Pin(23, Pin.OUT)  # Ausgangspin, der gesteuert werden soll

def web_page():
    with open('webserver.html', 'r') as f:
        html = f.read()
    return 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html

def handle_led_on():
    led_pin.on()
    return web_page()

def handle_led_off():
    led_pin.off()
    return web_page()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))

    if '/led_on' in request:
        response = handle_led_on()
    elif '/led_off' in request:
        response = handle_led_off()
    else:
        response = web_page()

    conn.send(response)
    conn.close()
