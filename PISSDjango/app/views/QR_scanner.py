import cv2
import datetime
import os
import re
from django.http import JsonResponse
from ..views.tokens import decode_token
import json


class QRScanner:
    def __init__(self):
        self.qr_code_detector = cv2.QRCodeDetector()

    def detect_qr_code(self, frame):
        """Detect and decode QR codes in the frame."""
        data, bbox, _ = self.qr_code_detector.detectAndDecode(frame)
        if data:
            return data, bbox
        return None, None

    def validate_data_format(self, data):
        """Validate the format of the QR code data."""
        pattern = r"^[0-9]{1}MI[0-9]{7}$"
        return re.match(pattern, data)

    def get_scanned_qr_codes(self):
        """Fetch the list of all scanned QR codes."""
        log_file_path = "QR_scanner/scanned_qr_codes.txt"
        data_list = []
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                for line in log_file:
                    code, timestamp = line.strip().split(" - ")
                    data_list.append({"code": code, "timestamp": timestamp})
        return data_list

    def generate_frames(self):
        """Yield frames with QR code detection for the video stream."""
        cap = cv2.VideoCapture(0)
        scanned_codes = set()
        log_file_path = "QR_scanner/scanned_qr_codes.txt"
        
        if not os.path.exists(log_file_path):
            open(log_file_path, 'w').close()

        while True:
            success, frame = cap.read()
            if not success:
                break

            data, bbox = self.detect_qr_code(frame)
            if data and data not in scanned_codes:
                if self.validate_data_format(data):  # Validate the data format
                    print(f"Valid QR Code detected: {data}")
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"Timestamp of detection: {timestamp}")
                    scanned_codes.add(data)

                    with open(log_file_path, "a") as log_file:
                        log_file.write(f"{data} - {timestamp}\n")

                    if bbox is not None:
                        bbox = bbox.astype(int)
                        for i in range(len(bbox[0])):
                            pt1 = tuple(bbox[0][i])
                            pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
                            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        cap.release()

def QR_scanner(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)

        token = data.get('token')
        if not token:
            return JsonResponse({"success": False, "message": "Token not provided."}, status=400)

        try:
            decoded_token = decode_token(token)
            user_id = decoded_token.get('user_id')
            role = decoded_token.get('role')
        except Exception:
            return JsonResponse({"success": False, "message": "Invalid token provided."}, status=400)

        # Ensure the user has the correct role (role == 2)
        if role != 2:
            return JsonResponse({"success": False, "message": "Insufficient role."}, status=403)

        # If token and role are valid, return all scanned QR codes
        scanner = QRScanner()
        data_list = scanner.get_scanned_qr_codes()
    return JsonResponse({"success": True, "scanned_codes": data_list}, status=200)