import cv2
import numpy as np
import pyautogui
import threading

# Inicializácia webkamery
cap = cv2.VideoCapture(0)

# Inicializácia premenných pre detekciu pohybu
frame_width = int(cap.get(2))
frame_height = int(cap.get(1))
fgbg = cv2.createBackgroundSubtractorMOG2()
min_contour_area = 600  # Minimálna plocha kontúry pre detekciu

# Premenná na sledovanie stavu pohybu
motion_detected = False

# Funkcia na kontrolu otvoreného okna Chrome a minimalizáciu
def minimize_chrome():
    while True:
        try:
            if motion_detected and "Google Chrome" in pyautogui.getActiveWindowTitle():
                pyautogui.hotkey("win", "down")
                pyautogui.hotkey("win", "down")
        except:
            pass

# Spustenie vlákna pre kontrolu Chrome okna
chrome_thread = threading.Thread(target=minimize_chrome)
chrome_thread.start()

ret, frame = cap.read()
if not ret:
    exit()

fgmask = fgbg.apply(frame)
_, thresh = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

motion_detected = False  # Resetujte stav pohybu

while True:
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            motion_detected = True  # Nastavenie stavu pohybu
            print("Detected door movement!")

    cv2.imshow("Door App", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
chrome_thread.join()
print("EXIT")
exit()
