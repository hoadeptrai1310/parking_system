import pygame
import time
from EmulatorGUI import GPIO  # Sử dụng GPIO giả lập

class LCD1602:
    def __init__(self, rs_pin, e_pin, data_pins):
        self.rs_pin = rs_pin
        self.e_pin = e_pin
        self.data_pins = data_pins

        # Thiết lập GPIO cho RS, E và các chân dữ liệu
        GPIO.setup(rs_pin, GPIO.OUT)
        GPIO.setup(e_pin, GPIO.OUT)
        for pin in data_pins:
            GPIO.setup(pin, GPIO.OUT)

        # Khởi tạo màn hình Pygame cho LCD
        pygame.init()
        self.screen = pygame.display.set_mode((250, 60))
        pygame.display.set_caption("LCD1602")
        self.font = pygame.font.Font(pygame.font.match_font('courier'), 24)
        self.lines = ["", ""]  # Lưu nội dung từng dòng
        self.backlight = True  # Giả lập đèn nền LCD
        self.cursor_position = [0, 0]
        self.cursor_visible = False

    def clear(self):
        self.lines = ["", ""]
        self.display()

    def write_command(self, cmd):
        GPIO.output(self.rs_pin, GPIO.LOW)  # Chuyển sang chế độ lệnh
        self.send(cmd)
        GPIO.output(self.e_pin, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(self.e_pin, GPIO.LOW)

    def write_data(self, data):
        GPIO.output(self.rs_pin, GPIO.HIGH)  # Chuyển sang chế độ dữ liệu
        self.send(data)
        GPIO.output(self.e_pin, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(self.e_pin, GPIO.LOW)

    def send(self, data):
    # Gửi 4 bit cao
        for i in range(4):
            GPIO.output(self.data_pins[i], GPIO.HIGH if (data >> (i + 4)) & 1 else GPIO.LOW)
            time.sleep(0.05)  # Tạo độ trễ để quan sát trạng thái
        # Gửi 4 bit thấp
        for i in range(4):
            GPIO.output(self.data_pins[i], GPIO.HIGH if (data >> i) & 1 else GPIO.LOW)
            time.sleep(0.05)  # Tạo độ trễ để quan sát trạng thái


    def write_string(self, text):
        if len(self.lines[0]) == 0:
            self.lines[0] = text[:16]  # Chỉ nhận 16 ký tự cho dòng đầu
        else:
            self.lines[1] = text[:16]  # Chỉ nhận 16 ký tự cho dòng thứ 2
        self.display()

    def display(self):
        """Hiển thị nội dung trên màn hình giả lập LCD."""
        self.screen.fill((0, 0, 0))  # Màu nền đen
        for i in range(2):
            text = self.lines[i]
            rendered_text = self.font.render(text, True, (0, 255, 0) if self.backlight else (50, 50, 50))
            if i == 0:
                self.screen.blit(rendered_text, (10, 2))  # Dòng đầu tiên
            else:
                self.screen.blit(rendered_text, (10, 30))  # Dòng thứ hai

        if self.cursor_visible:
            cursor_x = (10 + self.cursor_position[1] * 15) if self.cursor_position[0] == 1 else (0 + self.cursor_position[1] * 15)
            cursor_y = (30 if self.cursor_position[0] == 1 else 0)
            pygame.draw.line(self.screen, (255, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        pygame.display.flip()

    def set_cursor_position(self, row, col):
        self.cursor_position = [row, col]
        self.cursor_visible = True
        self.display()

    def hide_cursor(self):
        self.cursor_visible = False
        self.display()
