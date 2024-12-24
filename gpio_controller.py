from EmulatorGUI import GPIO  # Sử dụng GPIO giả lập từ EmulatorGUI
import time

def setup_gpio(pin, mode=GPIO.OUT):
    """Thiết lập chân GPIO."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, mode)

def open_gate(pin):
    """Mở cổng bằng cách kích hoạt relay."""
    print(f"Mở cổng sử dụng GPIO {pin}...")
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(5)  # Mở cổng trong 5 giây
    GPIO.output(pin, GPIO.LOW)
    print("Cổng đã đóng!")

def cleanup_gpio():
    """Dọn dẹp GPIO sau khi sử dụng."""
    GPIO.cleanup()

# Thêm một hàm theo dõi trạng thái GPIO
def print_gpio_status(pin):
    """In ra trạng thái của một chân GPIO."""
    status = GPIO.input(pin)
    print(f"Trạng thái của GPIO {pin}: {'HIGH' if status == GPIO.HIGH else 'LOW'}")
