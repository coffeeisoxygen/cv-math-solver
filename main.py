import cv2

from drawing import DrawingCanvas, process_drawing
from hand_detector import HandDetector, get_hand_info
from utils import init_camera


def main():
    """Fungsi utama program"""
    cap = init_camera()
    if cap is None:
        return

    detector = HandDetector()
    drawing_canvas = DrawingCanvas()
    debug = False  # Set True untuk menampilkan pesan debug

    try:
        while True:
            success, img = cap.read()
            if not success:
                print("Gagal membaca frame")
                break

            # Proses deteksi tangan
            hand_info = get_hand_info(img, detector, debug)

            # Proses drawing berdasarkan gesture
            img = process_drawing(img, hand_info, drawing_canvas, debug)

            # Tampilkan hasil
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
