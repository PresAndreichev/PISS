import qrcode
import cv2
import os

def generate_qr_code(data, filename):
    """
    Generate a QR code with the given data and save it as an image.

    :param data: The data to encode in the QR code.
    :param filename: The filename to save the QR code image.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"QR code saved as {filename}")

def scan_qr_code():
    """
    Scan QR codes using the webcam and print the decoded data.
    """
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    print("Starting QR code scanner. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Detect and decode
        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            print(f"Decoded Data: {data}")
            break

        # Display the frame
        cv2.imshow("QR Code Scanner", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def track_activity(data):
    """
    Track and log activity based on scanned QR code data.

    :param data: Decoded data from the QR code.
    """
    log_entry = f"{datetime.now()} - Activity: {data}\n"
    with open("activity_log.txt", "a") as log_file:
        log_file.write(log_entry)
    print(f"Activity logged: {log_entry.strip()}")

def main():
    """
    Main menu to generate or scan QR codes.
    """
    os.makedirs("qrcodes", exist_ok=True)

    while True:
        print("\n--- QR Code System ---")
        print("1. Generate QR Code for Attendance")
        print("2. Generate QR Code for Booking")
        print("3. Scan QR Code")
        print("4. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            user_id = input("Enter User ID for Attendance: ")
            filename = f"qrcodes/attendance_{user_id}.png"
            generate_qr_code(f"Attendance:{user_id}", filename)

        elif choice == '2':
            booking_id = input("Enter Booking ID: ")
            filename = f"qrcodes/booking_{booking_id}.png"
            generate_qr_code(f"Booking:{booking_id}", filename)

        elif choice == '3':
            scan_qr_code()

        elif choice == '4':
            print("Exiting QR Code System.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
