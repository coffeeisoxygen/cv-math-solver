from cvzone.HandTrackingModule import HandDetector as CVZoneHandDetector


class HandDetector:
    """Class untuk mendeteksi dan melacak tangan"""

    def __init__(self):
        self.detector = CVZoneHandDetector(
            staticMode=False,
            maxHands=1,
            modelComplexity=1,
            detectionCon=0.7,
            minTrackCon=0.5,
        )

    def detect_hands(self, img, draw=True):
        """Mendeteksi tangan dalam gambar"""
        return self.detector.findHands(img, draw=draw, flipType=True)

    def get_fingers_up(self, hand):
        """Mengambil jari yang sedang terangkat"""
        return self.detector.fingersUp(hand)

    def calculate_finger_distance(self, lm_list, img, debug=False):
        """Menghitung jarak antara jari telunjuk dan jari tengah"""
        if lm_list is not None and len(lm_list) > 12:
            length, info, img = self.detector.findDistance(
                lm_list[8][0:2], lm_list[12][0:2], img, color=(255, 0, 255), scale=10
            )
            if debug:
                print(f"Distance between fingers: {length}")
            return length, img
        return None, img


def get_hand_info(img, detector, debug=False):
    """Mendapatkan informasi tangan dari gambar"""
    hands, img = detector.detect_hands(img)

    if hands:
        hand = hands[0]
        lm_list = hand["lmList"]
        fingers = detector.get_fingers_up(hand)

        if debug:
            print(f"Fingers: {fingers}")

        return {"fingers": fingers, "lm_list": lm_list, "detected": True}
    else:
        return {"detected": False, "fingers": None, "lm_list": None}
