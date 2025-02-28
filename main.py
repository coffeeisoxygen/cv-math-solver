import cv2
from cvzone.HandTrackingModule import HandDetector


def init_camera(width=640, height=480):
    """Inisialisasi dan setup kamera"""
    cap = cv2.VideoCapture(0)
    cap.set(3, width)  # Width
    cap.set(4, height)  # Height
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  # Make window resizable

    if not cap.isOpened():
        print("Error: Tidak dapat mengakses kamera")
        return None
    return cap


def setup_detector():
    """Inisialisasi hand detector"""
    return HandDetector(
        staticMode=False,
        maxHands=1,
        modelComplexity=1,
        detectionCon=0.7,
        minTrackCon=0.5,
    )


def get_hand_info(img, detector, debug=False):
    """Mendapatkan informasi tangan dari gambar"""
    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        hand = hands[0]
        lm_list = hand["lmList"]
        fingers = detector.fingersUp(hand)
        if debug:
            print(f"Fingers: {fingers}")
        return fingers, lm_list, img
    else:
        return None, None, img


def calculate_finger_distance(lm_list, img, detector, debug=False):
    """Menghitung jarak antar jari"""
    if lm_list is not None and len(lm_list) > 12:
        length, info, img = detector.findDistance(
            lm_list[8][0:2], lm_list[12][0:2], img, color=(255, 0, 255), scale=10
        )
        if debug:
            print(f"Distance between fingers: {length}")
        return length, img
    return None, img


def draw(info, img, prev_pos):
    fingers, lm_list = info
    current_pos = None

    # deteksi jika hanya jari telunjuk
    if fingers == [0, 1, 0, 0, 0]:
        current_pos = lm_list[8][0:2]
        if prev_pos is None:
            prev_pos = current_pos
        cv2.line(img, prev_pos, current_pos, (0, 255, 0), 2)
        prev_pos = current_pos

    return prev_pos



def main():
    """Fungsi utama program"""
    cap = init_camera()
    if cap is None:
        return

    detector = setup_detector()
    debug = True  # Set False untuk menghilangkan pesan debug
    prev_pos = None

    try:
        while True:
            success, img = cap.read()
            if not success:
                print("Gagal membaca frame")
                break

            # Proses deteksi tangan
            fingers, lm_list, img = get_hand_info(img, detector, debug)

            # Hitung jarak jari jika tangan terdeteksi
            if lm_list is not None:
                _, img = calculate_finger_distance(lm_list, img, detector, debug)

            # Tampilkan hasil jika img tidak None
            if img is not None:
                cv2.imshow("Image", img)

            # Keluar dari loop jika 'q' ditekan
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        # Pastikan resources dibersihkan
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
