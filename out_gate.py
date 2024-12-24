import tkinter as tk
from tkinter.filedialog import askopenfilename
import gpio_controller as gpio
import log_manager as log
import license_plate_recognition as lpr
from pnhLCD1602 import LCD1602  # Import lớp LCD đã cập nhật
from EmulatorGUI import GPIO  # Sử dụng GPIO giả lập từ EmulatorGUI
import time

# Thiết lập GPIO cho cổng ra, LCD, và LED báo động
out_gate_pin = 18
alarm_led_pin = 23  # GPIO cho LED báo động
gpio.setup_gpio(out_gate_pin)
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

# Kiểm tra và xóa biển số khỏi log
for plate in detected_plates:
    if plate in log.load_license_plates('plate_log.csv'):
        print(f"Biển số {plate} hợp lệ. Mở cổng.")
        log.remove_plate(plate)  # Xóa biển số khỏi log
        lcd.clear()  # Xóa màn hình trước khi hiển thị nội dung mới
        lcd.write_string(f"Xe ra: {plate}")
        lcd.display()  # Cập nhật LCD
        time.sleep(2)  # Tạm dừng để nội dung hiển thị đủ thời gian
        gpio.open_gate(out_gate_pin)  # Mở cổng ra
        GPIO.output(alarm_led_pin, GPIO.LOW)  # Tắt LED báo động khi biển số hợp lệ
    else:
        print(f"Biển số {plate} không hợp lệ. Bật đèn báo động.")
        lcd.clear()  # Xóa màn hình trước khi hiển thị
        lcd.write_string("Khong hop le")
        lcd.display()  # Cập nhật LCD
        time.sleep(2)  # Tăng thời gian hiển thị để người dùng nhìn thấy
        GPIO.output(alarm_led_pin, GPIO.HIGH)  # Bật LED báo động

# Dọn dẹp GPIO và LCD sau khi sử dụng
gpio.cleanup_gpio()
lcd.clear()
