import machine
import time

uart = machine.UART(1, baudrate=9600, tx=17, rx=16)

def send_module_name(module_name):
    while True:
        uart.write("ifsdpo9ij\r")
        uart.write(module_name.encode())
        time.sleep(1)

while True:
    # Replace 'YourModuleName' with the actual name of the module
    send_module_name("YourModuleName")
    time.sleep(1)
    # Wait for confirmation code from the main ESP
    confirmation_code = uart.readline()
    if confirmation_code and confirmation_code.startswith(b"CONFIRM:"):
        module_name = confirmation_code[len("CONFIRM:"):]
        print("Confirmation received for module:", module_name)
        # Switch to the module-specific program here
        break
