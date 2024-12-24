import torch
import cv2
import function.helper as helper

# Tải model YOLOv5
yolo_LP_detect = torch.hub.load('yolov5', 'custom', path='model/LP_detector_nano_61.pt', source='local')
yolo_license_plate = torch.hub.load('yolov5', 'custom', path='model/LP_ocr_nano_62.pt', source='local')

def detect_license_plate(image_path):
    """Phát hiện biển số trong ảnh và trả về danh sách biển số."""
    img = cv2.imread(image_path)
    plates = yolo_LP_detect(img, size=640)
    list_plates = plates.pandas().xyxy[0].values.tolist()
    
    detected_plates = set()
    for plate in list_plates:
        x_min, y_min, x_max, y_max = int(plate[0]), int(plate[1]), int(plate[2]), int(plate[3])
        crop_img = img[y_min:y_max, x_min:x_max]
        lp_text = helper.read_plate(yolo_license_plate, crop_img)
        if lp_text != "unknown":
            detected_plates.add(lp_text)
    
    return detected_plates
