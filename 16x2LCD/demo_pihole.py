# Simple string program. Writes and updates strings.
# Gets the hostname and Ip address using built in python libraries.
# Demo program for the I2C 16x2 Display from Dealextreme
# Created by Bradley Gillap based on work from The Raspberry Pi Guy YouTube channel

# Import necessary libraries for commuunication and display use
import lcddriver  # Driver
import socket  # For host and IP
import time  # For general timers. Sleep etc.
import fcntl  # For host and IP
import struct
import json  # For pihole API
import urllib.request  # For pihole API


# Initialize IP Address Check
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])


# Initialize Hostname Check
socket.gethostbyname(socket.gethostname())

# VARIABLES
# If you use something from the driver library use the "display." prefix first

display = lcddriver.lcd()  # Load lcddriver and set it to display
ipaddy = get_ip_address('eth0')  # Define Ip address variable
url = ("http://" + str(ipaddy) + "/admin/api.php")  # Connect to pihole API

# Populate data variable with API info
data = json.load(urllib.request.urlopen(url))

display.lcd_display_string("PI-HOLE NETWORK", 1)
display.lcd_display_string("WIDE PROTECTION", 2)
display.backlight_on()
time.sleep(10)
display.backlight_off()

try:

    while True:

        data = json.load(urllib.request.urlopen(url))  # Load API data
        blocked = data['ads_blocked_today']  # Assign API Data to variables
        percent = data['ads_percentage_today']
        queries = data['dns_queries_today']
        domains = data['domains_being_blocked']
        clients = data['unique_clients']
        status = data['status']

        display.lcd_clear()
        # Show host on screen max 16 chars
        display.lcd_display_string("Host:" + str((socket.gethostname())), 1)
        # Show IP address on screen max 16 chars
        display.lcd_display_string("IP:" + str(ipaddy), 2)
        time.sleep(4)  # Wait

        display.lcd_clear()
        display.lcd_display_string("Status:" + str(status), 1)
        display.lcd_display_String("Clients:" + str(clients), 2)
        time.sleep(4)

        display.lcd_clear()  # Clear the screen
        # Show sites blocked on screen max 16 chars
        display.lcd_display_string("Blocked:" + str(blocked), 1)
        # Show percentage of sites blocked max 16 chars
        display.lcd_display_string(
            "Percent:" + "{:.3f}".format(percent)+"%", 2)
        time.sleep(4)

        display.lcd_clear()
        # Show total queries on screen max 16 chars
        display.lcd_display_string("Queries:" + str(queries), 1)
        # Show total domains in blocklist max 16 chars
        display.lcd_display_string("Domains:" + str(domains), 2)
        time.sleep(4)
        display.lcd_clear()

# If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()
