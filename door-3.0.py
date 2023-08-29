import cv2
import pyautogui
import time

cap = cv2.VideoCapture(0)

# ukoncenie prechadzajucich procesov ak zostali vysiet
cap.release()
cv2.destroyAllWindows()

# oneskoreny start
time.sleep(10)

# Inicializácia webkamery
cap = cv2.VideoCapture(0)

# Inicializácia premenných pre detekciu pohybu
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fgbg = cv2.createBackgroundSubtractorMOG2()
min_contour_area = 350

# Premenná na sledovanie stavu pohybu
motion_detected = False
det = 0
paused = False  # Initially not paused

# Oblast snimania
x1 = 550  # vzdialenost v pixeloch od laveho okraja kamery = zaciatok oblasti
h1 = 225  # vzdialenost v pixeloch od horneho okraja kamery = zaciatok oblasti
y1 = 300  # vzdialenost v pixeloch od horneho okraja kamery = zaciatok oblasti
w1 = 610  # vzdialenost v pixeloch od laveho okraja kamery = koniec oblasti

while True:
    ret, frame = cap.read()
    crop = frame[h1:y1, x1:w1]
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
                cv2.rectangle(crop, (x, y), (x + w, y + h), (0, 255, 0), 2)
                motion_detected = True
                det = det + 1
                print(det)
                print("Detected door movement!")

    if det > 15 and not paused:
        #paused = True  # Enter paused state
        #pyautogui.hotkey("win", "d")
        print("Paused. Press 'b' to resume or 'q' to exit.")
        print(time.ctime())

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
        cv2.putText(frame, "paused", (x1 - 20, h1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        cv2.putText(frame, str(det), (x1 - 10, h1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    cv2.rectangle(frame, (x1, y1), (w1, h1), (0, 0, 255), 2)
    cv2.imshow("Door App", frame)

    #if det > 20:
        #pyautogui.hotkey("win", "d")
        #break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("EXIT")
exit()
