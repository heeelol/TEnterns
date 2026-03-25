from dataclasses import dataclass
from typing import Any, List
import importlib
import math

import cv2
import mediapipe as mp


def _resolve_hands_class():
    solutions = getattr(mp, "solutions", None)
    if solutions is not None and hasattr(solutions, "hands"):
        return solutions.hands.Hands

    hands_module = importlib.import_module("mediapipe.python.solutions.hands")
    return hands_module.Hands


@dataclass
class HandLandmarkResult:
    handedness: str
    landmarks: List[Any]
    is_grabbing: bool
    grab_score: float


class HandTracker:
    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        hands_class = _resolve_hands_class()
        self._hands = hands_class(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    @staticmethod
    def _distance(a, b) -> float:
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)

    def _estimate_grab_status(self, landmarks: List[Any]) -> tuple[bool, float]:
        wrist = landmarks[0]
        palm_anchor = landmarks[9]
        palm_size = max(self._distance(wrist, palm_anchor), 1e-6)

        palm_center_x = (landmarks[0].x + landmarks[5].x + landmarks[9].x + landmarks[13].x + landmarks[17].x) / 5.0
        palm_center_y = (landmarks[0].y + landmarks[5].y + landmarks[9].y + landmarks[13].y + landmarks[17].y) / 5.0
        palm_center_z = (landmarks[0].z + landmarks[5].z + landmarks[9].z + landmarks[13].z + landmarks[17].z) / 5.0

        class _Point:
            def __init__(self, x: float, y: float, z: float) -> None:
                self.x = x
                self.y = y
                self.z = z

        palm_center = _Point(palm_center_x, palm_center_y, palm_center_z)

        tip_ids = [4, 8, 12, 16, 20]
        normalized_tip_distances = [self._distance(landmarks[idx], palm_center) / palm_size for idx in tip_ids]

        curled_count = sum(distance < 1.15 for distance in normalized_tip_distances)
        grab_score = curled_count / len(tip_ids)
        is_grabbing = curled_count >= 4
        return is_grabbing, grab_score

    def detect(self, frame_bgr):
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self._hands.process(frame_rgb)

        detections: List[HandLandmarkResult] = []
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, hand_type in zip(results.multi_hand_landmarks, results.multi_handedness):
                landmarks = list(hand_landmarks.landmark)
                is_grabbing, grab_score = self._estimate_grab_status(landmarks)
                detections.append(
                    HandLandmarkResult(
                        handedness=hand_type.classification[0].label,
                        landmarks=landmarks,
                        is_grabbing=is_grabbing,
                        grab_score=grab_score,
                    )
                )
        return detections
