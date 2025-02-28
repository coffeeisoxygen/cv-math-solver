import cv2
from cvzone.HandTrackingModule import HandDetector

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
if not cap.isOpened():
    print("Error: Tidak dapat mengakses kamera")
    exit()

detector = HandDetector(
    staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5
)

while True:
    success, img = cap.read()
    if not success:
        print("Gagal membaca frame dari kamera")
        break

    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        center1 = hand1["center"]
        handType1 = hand1["type"]

        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        # # Tambahkan pengecekan indeks
        # if len(lmList1) > 12:  # Pastikan indeks 8 dan 12 tersedia
        #     length, info, img = detector.findDistance(
        #         lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255), scale=10
        #     )
        #     print(length)

    if img is not None:
        cv2.imshow("Image", img)
    else:
        print("Error: Image could not be displayed - img is None")

    # Tambahkan cara untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Bersihkan saat program selesai
cap.release()
cv2.destroyAllWindows()
