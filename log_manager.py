import csv

def load_license_plates(csv_file):
    """Tải danh sách biển số từ file CSV."""
    valid_plates = set()
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            valid_plates.add(row[0])
    return valid_plates

def log_plate(lp_text, csv_file='plate_log.csv'):
    """Ghi biển số vào file CSV."""
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([lp_text])

def remove_plate(lp_text, csv_file='plate_log.csv'):
    """Xóa biển số khỏi file CSV."""
    lines = []
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        lines = [row for row in reader if row[0] != lp_text]
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)
