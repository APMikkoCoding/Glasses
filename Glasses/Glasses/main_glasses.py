from gpiozero import Servo
import time
import board
import busio
import digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import socket

class Screen:
    def __init__(self):
        self.WIDTH = 128
        self.HEIGHT = 32
        self.BORDER = 5
        self.oled_reset = digitalio.DigitalInOut(board.D4)
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=0x3c, reset=self.oled_reset)

    def clear_display(self):
        self.oled.fill(0)
        self.oled.show()

    def create_canvas(self):
        self.image = Image.new('1', (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)
        self.font = ImageFont.truetype('PixelOperator.ttf', 16)

    def write_text(self, text):
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        self.draw.text((0, 0), text, font=self.font, fill=255)
        self.oled.image(self.image)
        self.oled.show()

class ServoController:
    def __init__(self):
        self.servo = Servo(4)

    def move_up(self):
        self.servo.value = 0.9

    def move_down(self):
        self.servo.value = -1

class Camera:
    def __init__(self):
        pass

class Server:
    def __init__(self, server_ip):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = 5050
        self.IP = server_ip

    def connect_to_server(self):
        self.server.connect((self.IP, self.PORT))

    def send_data(self, data):
        self.server.send(data)

    def recv_data(self):
        return self.server.recv(1024)

    def close_server(self):
        self.server.close()

class Process:
    def __init__(self):
        self.servo = ServoController()
        self.display = Screen()

    def process_data(self, data: bytes):
        data = data.decode('utf-8')
        if 'SERVO' in data:
            if data == 'SERVO: DOWN':
                self.servo.move_down()

            elif data == 'SERVO: UP':
                self.servo.move_up()

        elif 'DISPLAY' in data:
            text = data.split(': ')[1]
            self.display.clear_display()
            self.display.create_canvas()
            self.display.write_text(text)

server = Server(input('Server IP: '))
process = Process()
server.connect_to_server()
data = server.recv_data()
process.process_data(data)
server.close_server()