import machine
import time
import uos

uart = machine.UART(1, baudrate=9600, tx=17, rx=16)

def send_confirmation_code(module_name):
    confirmation_code = "CONFIRM:" + module_name
    uart.write(confirmation_code)

while True:
    if uart.any():
        print("test")
        received_data = uart.readline()
        if received_data:
            module_name = received_data.decode().strip()
            print("Module connected:", module_name)
            send_confirmation_code(module_name)
            time.sleep(1)  # Wait for the confirmation code to be sent
            # Switch to the module-specific program here
            uos.exec("module_{}.py".format(module_name))
    time.sleep(0.1)

