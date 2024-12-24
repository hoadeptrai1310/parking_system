from PIL import Image
import cv2
import torch
import math 
import function.utils_rotate as utils_rotate
import function.helper as helper
import os
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Sử dụng Tkinter để mở cửa sổ chọn tệp
Tk().withdraw()  # Ẩn cửa sổ chính của Tkinter
image_path = askopenfilename(title='Chọn ảnh', filetypes=[("Image files", "*.jpg *.jpeg *.png")])

# Kiểm tra xem người dùng đã chọn tệp hay chưa
if not image_path:
    print("Bạn chưa chọn tệp nào.")
    exit()

# Tạo thư mục 'result' nếu chưa tồn tại
result_dir = 'result'
os.makedirs(result_dir, exist_ok=True)

# Lấy tên tệp từ đường dẫn
image_name = os.path.basename(image_path)

# Đường dẫn lưu kết quả
output_path = os.path.join(result_dir, image_name)

# Tải các mô hình YOLOv5 từ thư mục yolov5
yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector.pt', force_reload=True, source='local')
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr.pt', force_reload=True, source='local')
yolo_license_plate.conf = 0.60

# Đọc ảnh đã chọn
img = cv2.imread(image_path)
plates = yolo_LP_detect(img, size=640)

list_plates = plates.pandas().xyxy[0].values.tolist()
list_read_plates = set()
if len(list_plates) == 0:
    lp = helper.read_plate(yolo_license_plate, img)
    if lp != "unknown":
        cv2.putText(img, lp, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        list_read_plates.add(lp)
else:
    for plate in list_plates:
        flag = 0
        x = int(plate[0])  # xmin
        y = int(plate[1])  # ymin
        w = int(plate[2] - plate[0])  # xmax - xmin
        h = int(plate[3] - plate[1])  # ymax - ymin  
        crop_img = img[y:y + h, x:x + w]
        cv2.rectangle(img, (int(plate[0]), int(plate[1])), (int(plate[2]), int(plate[3])), color=(0, 0, 225), thickness=2)
        cv2.imwrite("crop.jpg", crop_img)
        rc_image = cv2.imread("crop.jpg")
        lp = ""
        for cc in range(0, 2):
            for ct in range(0, 2):
                lp = helper.read_plate(yolo_license_plate, utils_rotate.deskew(crop_img, cc, ct))
                if lp != "unknown":
                    list_read_plates.add(lp)
                    cv2.putText(img, lp, (int(plate[0]), int(plate[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                    flag = 1
                    break
            if flag == 1:
                break

# Lưu ảnh đã xử lý vào thư mục 'result' với tên tệp không thay đổi
cv2.imwrite(output_path, img)

# Hiển thị ảnh
cv2.imshow('frame', img)
cv2.waitKey()
cv2.destroyAllWindows()

print(f"Ảnh đã được lưu vào {output_path}")
