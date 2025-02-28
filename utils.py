import cv2


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
