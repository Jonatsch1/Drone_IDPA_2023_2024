import network
import machine
from machine import PWM, Pin
import usocket as socket
import time

# SSID und Passwort für den WiFi Access Point
SSID = "Drohne_IDPA"
PASSWORD = "IDPA2024"

# Setup des WiFi Access Points
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID, password=PASSWORD)

# Setup des Servos
sg90 = PWM(Pin(22, mode=Pin.OUT))
sg90.freq(50)


# Funktion zur Servosteuerung
def set_servo_angle(angle):
    duty = int(((100 - angle) / 100) * 23) + 100  # Berechnung des Duty-Zyklus basierend auf dem Winkel
    print(angle)
    print(duty)
    sg90.duty(duty)


# Funktion zum Parsen der HTTP-Anfragen
def parse_request(request):
    parsed = request.split(" ")
    method = parsed[0]
    path = parsed[1]
    return method, path


# Funktion zum Laden der Datei
def load_file(filename, mode='r'):
    try:
        with open(filename, mode) as file:
            return file.read()
    except Exception as e:
        print("Fehler beim Laden der Datei:", e)


# Funktion zum Senden einer HTTP-Antwort
def send_response(conn, content, content_type):
    try:
        conn.send("HTTP/1.1 200 OK\r\n")
        conn.send("Content-Type: {}\r\n".format(content_type))
        conn.send("Connection: close\r\n\r\n")
        conn.sendall(content)
    except Exception as e:
        print("Fehler beim Senden der Antwort:", e)


# Funktion zum Neustarten des Geräts
def reboot():
    print("Gerät wird neu gestartet...")
    machine.reset()


# Funktion zum Starten des Webservers
def start_webserver():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print("Webserver gestartet")

    while True:
        try:
            time.sleep(0.01)
            conn, addr = s.accept()
            print('Verbunden mit %s' % str(addr))
            request = conn.recv(1024)
            method, path = parse_request(request.decode('utf-8'))
            print('HTTP request:', method, path)

            if path == "/":
                html_content = load_file("webserver_Modul1.html")
                send_response(conn, html_content, "text/html")
            elif path.startswith("/setServo"):
                angle = int(path.split("=")[1])
                set_servo_angle(angle)
                send_response(conn, "Servo angle set to: {}".format(angle), "text/html")
            elif path == "/Greifer.png":
                image_content = load_file("Greifer.png", 'rb')
                send_response(conn, image_content, "image/png")

            conn.close()
        except Exception as e:
            print("Fehler:", e)
            reboot()


# Starten des Webservers
set_servo_angle(0)
start_webserver()

