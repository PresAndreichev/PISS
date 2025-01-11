from flask import Flask, render_template, Response
import cv2
import datetime
import os, re

app = Flask(__name__)

class QRScanner:
    def __init__(self):
        self.qr_code_detector = cv2.QRCodeDetector()

    def detect_qr_code(self, frame):
        """Detect and decode QR codes in the frame."""
        data, bbox, _ = self.qr_code_detector.detectAndDecode(frame)
        if data:
            return data, bbox
        return None, None

scanner = QRScanner()

log_file_path = "QR_scanner/scanned_qr_codes.txt"
if not os.path.exists(log_file_path):
    open(log_file_path, 'w').close()

def validate_data_format(data):
    """Validate if the data matches the format [0-9]{1}MI[0-9]{6}."""
    pattern = r"^[0-9]{1}MI[0-9]{7}$"
    return re.match(pattern, data)


def generate_frames():
    """Yield frames with QR code detection for the video stream."""
    cap = cv2.VideoCapture(0)
    scanned_codes = set()

    while True:
        success, frame = cap.read()
        if not success:
            break

        data, bbox = scanner.detect_qr_code(frame)
        if data and data not in scanned_codes:
            if validate_data_format(data):  # Validate the data format
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
            else:
                print(f"Ignored QR Code with invalid format: {data}")

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Provide the video feed to the frontend."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
