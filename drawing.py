import cv2
import numpy as np


class DrawingState:
    """Enum untuk status drawing"""

    IDLE = 0  # Tidak menggambar
    DRAWING = 1  # Sedang menggambar
    PAUSED = 2  # Jeda menggambar
    STOPPED = 3  # Berhenti menggambar


class DrawingCanvas:
    """Class untuk membuat dan mengelola canvas gambar"""

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), np.uint8)
        self.prev_point = None
        self.state = DrawingState.IDLE
        self.color = (0, 255, 0)  # Default: hijau
        self.thickness = 2

    def clear_canvas(self):
        """Membersihkan canvas"""
        self.canvas = np.zeros((self.height, self.width, 3), np.uint8)

    def draw_line(self, point):
        """Menggambar garis dari titik sebelumnya ke titik saat ini"""
        if self.prev_point is not None and self.state == DrawingState.DRAWING:
            cv2.line(self.canvas, self.prev_point, point, self.color, self.thickness)
        self.prev_point = point

    def update_state(self, fingers):
        """Memperbarui status menggambar berdasarkan posisi jari"""
        if fingers is None:
            self.state = DrawingState.IDLE
            return

        # Index finger only [0,1,0,0,0] - Drawing mode
        if fingers == [0, 1, 0, 0, 0]:
            self.state = DrawingState.DRAWING

        # Index and middle fingers [0,1,1,0,0] - Pause drawing
        elif fingers == [0, 1, 1, 0, 0]:
            self.state = DrawingState.PAUSED
            self.prev_point = None  # Reset previous point to avoid connecting lines

        # Index, middle, and ring fingers [0,1,1,1,0] - Stop drawing
        elif fingers == [0, 1, 1, 1, 0]:
            self.state = DrawingState.STOPPED
            self.clear_canvas()
            self.prev_point = None


def process_drawing(img, hand_info, drawing_canvas, debug=False):
    """Memproses gambar untuk menggambar berdasarkan gestur tangan"""
    # Overlay the canvas onto the image
    img_with_drawing = img.copy()

    # Check if hand is detected
    if hand_info["detected"]:
        fingers = hand_info["fingers"]
        lm_list = hand_info["lm_list"]

        # Update the drawing state based on fingers
        drawing_canvas.update_state(fingers)

        if debug:
            state_text = ["IDLE", "DRAWING", "PAUSED", "STOPPED"][drawing_canvas.state]
            cv2.putText(
                img_with_drawing,
                f"State: {state_text}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2,
            )

        # Draw if in DRAWING state and index finger is up
        if drawing_canvas.state == DrawingState.DRAWING:
            # Get index finger tip position
            index_finger_tip = tuple(map(int, lm_list[8][0:2]))
            drawing_canvas.draw_line(index_finger_tip)

    # Overlay drawing on the original image
    img_with_drawing = cv2.addWeighted(img_with_drawing, 1, drawing_canvas.canvas, 1, 0)

    return img_with_drawing
