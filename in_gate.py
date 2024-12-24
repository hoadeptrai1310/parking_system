import tkinter as tk
from tkinter.filedialog import askopenfilename
import gpio_controller as gpio
import license_plate_recognition as lpr
import log_manager as log
from pnhLCD1602 import LCD1602  # Import lớp LCD đã cập nhật
from EmulatorGUI import GPIO  # Sử dụng GPIO giả lập từ EmulatorGUI
import time

# Thiết lập GPIO cho cổng vào, LCD, và LED báo động
in_gate_pin = 17
alarm_led_pin = 23  # GPIO cho LED báo động
gpio.setup_gpio(in_gate_pin)
gpio.setup_gpio(alarm_led_pin)

# Thiết lập các chân cho LCD
lcd_rs_pin = 5
lcd_e_pin = 6
lcd_data_pins = [12, 16, 20, 21]
lcd = LCD1602(rs_pin=lcd_rs_pin, e_pin=lcd_e_pin, data_pins=lcd_data_pins)  # Khởi tạo đối tượng LCD

# Chọn file ảnh
def select_image_file():
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính
    file_path = askopenfilename(title="Chọn ảnh", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    root.destroy()  # Đóng cửa sổ sau khi chọn file
    return file_path

image_path = select_image_file()
if not image_path:
    print("Không chọn file ảnh, thoát.")
    exit()

# Phát hiện biển số
detected_plates = lpr.detect_license_plate(image_path)

# Ghi biển số vào log và mở cổng
for plate in detected_plates:
    log.log_plate(plate)
    lcd.clear()  # Xóa màn hình trước khi hiển thị nội dung mới
    lcd.write_string(f"Xe vao: {plate}")
    lcd.display()  # Cập nhật LCD
    time.sleep(2)  # Thời gian ngủ để đảm bảo hiển thị trên LCD
    gpio.open_gate(in_gate_pin)  # Mở cổng vào
    GPIO.output(alarm_led_pin, GPIO.LOW)  # Tắt LED báo động khi biển số hợp lệ

# Dọn dẹp GPIO và LCD sau khi sử dụng
gpio.cleanup_gpio()
lcd.clear()
