import cv2
from simple_facerec import SimpleFacerec
import time

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Load Camera
cap = cv2.VideoCapture(0)

# Initialize cheating status and timer
cheating_status = "Not Cheated"
unknown_detected_time = None

while True:
    ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    
    # Variable to track if cheating is detected in the current frame
    cheating_detected = False

    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        if name == "Unknown":
            if unknown_detected_time is None:
                unknown_detected_time = time.time()
                print("Unknown face detected. Starting timer.")
            else:
                elapsed_time = time.time() - unknown_detected_time
                print(f"Unknown face detected for {elapsed_time:.2f} seconds")
                if elapsed_time > 5:
                    cheating_detected = True
                    print("Cheating detected!")
            cv2.putText(frame, "Unknown", (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    # Update cheating status if any unknown face is detected for more than 1 second
    if cheating_detected:
        cheating_status = "Cheated"
    else:
        if not any(name == "Unknown" for name in face_names):
            unknown_detected_time = None

    # Clear the current console line and print the updated status
    print(f"\r{' '*50}", end='')  # Clear the line with spaces
    print(f"\rCheating Status: {cheating_status}", end='')

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
