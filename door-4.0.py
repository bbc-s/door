import cv2
import pyautogui
import time

cap = cv2.VideoCapture(0)

# ukoncenie prechadzajucich procesov ak zostali vysiet
cap.release()
cv2.destroyAllWindows()

# oneskoreny start
time.sleep(1)

# Inicializácia webkamery
cap = cv2.VideoCapture(0)

# Inicializácia premenných pre detekciu pohybu
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fgbg = cv2.createBackgroundSubtractorMOG2()
min_contour_area = 200

# Premenná na sledovanie stavu pohybu
motion_detected = False
det = 0
dettime = ""
no_motion_timer = time.time()
paused = False  # Initially not paused

# Oblast snimania
x1 = 550  # vzdialenost v pixeloch od laveho okraja kamery = zaciatok oblasti
h1 = 225  # vzdialenost v pixeloch od horneho okraja kamery = zaciatok oblasti
y1 = 300  # vzdialenost v pixeloch od horneho okraja kamery = zaciatok oblasti
w1 = 610  # vzdialenost v pixeloch od laveho okraja kamery = koniec oblasti

while True:
    ret, frame = cap.read()
    crop = cv2.cvtColor(frame[h1:y1, x1:w1], cv2.COLOR_BGR2GRAY)
    if not ret:
        break

    if not paused:
        # Detekcia pohybu v zmenšenej snímke
        fgmask = fgbg.apply(crop)
        _, thresh = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        if cv2.waitKey(2) & 0xFF == ord("r"):
            det = 0
            print(det)

        for contour in contours:
            if cv2.contourArea(contour) > min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x + x1, y + h1), (x + x1 + w, y + h1 + h), (0, 255, 0), 2)
                motion_detected = True
                det = det + 1
                no_motion_timer = time.time()  # Reset no motion timer
                print(det)
                print("Detected door movement!")
    
    # Check if no motion has been detected for more than 5 seconds
    if not motion_detected and time.time() - no_motion_timer > 5 and det > 0 < 15:
        det = 0
        print("Resetting det due to no motion")
        no_motion_timer = time.time()

    if det > 15 and not paused:
        paused = True  # Enter paused state
        pyautogui.hotkey("win", "d")
        dettime = str(time.ctime())
        print("Paused. Press 'b' to resume or 'q' to exit.")
        print(time.ctime())

        # Save the log entry with a timestamp
        with open("G:/Desktop/python/door/log.txt", "a") as log_file:
            log_file.write(f"Door opened: {dettime}\n")
    
    if cv2.waitKey(1) & 0xFF == ord("b"):
        paused = not paused  # Toggle the paused status
        if paused:
            print("Paused")
        else:
            det = 0
            print(det)
            print("Resumed")

    # Display "paused" on the frame if paused
    if paused:
        cv2.putText(frame, "paused", (x1 - 20, h1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, str("detected: " + dettime), (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    else:
        cv2.putText(frame, str(det), (x1 - 10, h1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.putText(frame, "b = pause", (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "r = reset", (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "q = quit", (0, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.rectangle(frame, (x1, y1), (w1, h1), (0, 0, 255), 2)
    cv2.imshow("Door App", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("EXIT")
exit()
