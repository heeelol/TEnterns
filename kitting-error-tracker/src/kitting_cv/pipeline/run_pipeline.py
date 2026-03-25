import cv2

from kitting_cv.segmentation import BinSegmenter
from kitting_cv.tracking import HandTracker


def _draw_hand_coordinates(frame, hand_detections) -> None:
    if not hand_detections:
        return

    frame_h, frame_w = frame.shape[:2]

    colors = [(0, 200, 255), (255, 120, 0)]

    for hand_idx, hand in enumerate(hand_detections[:2]):
        status_text = "GRAB" if hand.is_grabbing else "OPEN"
        top_y = 70 + hand_idx * 18
        cv2.putText(
            frame,
            f"Hand {hand_idx + 1} ({hand.handedness}) {status_text} score={hand.grab_score:.2f}",
            (20, top_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 0),
            1,
        )

        panel_x = 20 + hand_idx * 360
        for landmark_idx, landmark in enumerate(hand.landmarks):
            x_px = int(landmark.x * frame_w)
            y_px = int(landmark.y * frame_h)

            color = colors[hand_idx % len(colors)]
            cv2.circle(frame, (x_px, y_px), 3, color, -1)
            cv2.putText(
                frame,
                f"H{hand_idx + 1}:{landmark_idx}",
                (x_px + 4, y_px - 4),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                color,
                1,
            )

            line_y = 110 + landmark_idx * 14
            cv2.putText(
                frame,
                f"{landmark_idx:02d}: ({landmark.x:.3f}, {landmark.y:.3f}, {landmark.z:.3f})",
                (panel_x, line_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (255, 255, 255),
                1,
            )


def run_camera_pipeline(camera_index: int = 0) -> None:
    hand_tracker = HandTracker(max_num_hands=2)
    bin_segmenter = BinSegmenter()

    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        raise RuntimeError("Could not open camera.")

    while True:
        ok, frame = capture.read()
        if not ok:
            break

        hand_detections = hand_tracker.detect(frame)
        bin_mask = bin_segmenter.segment(frame)

        cv2.putText(
            frame,
            f"Hands detected: {len(hand_detections)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2,
        )

        _draw_hand_coordinates(frame, hand_detections)

        cv2.imshow("kitting-camera", frame)
        cv2.imshow("bin-mask", bin_mask)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()
