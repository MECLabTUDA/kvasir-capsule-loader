from typing import Optional

import numpy as np
from PIL import Image

from .bbox import BoundingBox
from .config import KVASIR_CAPSULE_PATH
from .types import FindingCategory, FindingClass, findingclass_to_dirname


class KvasirCapsuleSample:
    """
    Abstraction for a single image + bbox + label record.
    """

    def __init__(
        self,
        filename: str,
        video_id: str,
        frame_number: int,
        finding_category: FindingCategory,
        finding_class: FindingClass,
        bbox: Optional[BoundingBox] = None,
    ):
        self.filename = filename
        self.video_id = video_id
        self.frame_id = frame_number
        self.finding_category = finding_category
        self.finding_class = finding_class
        self.bbox = bbox

    def load_image(self) -> np.ndarray:
        """
        Load and return the image as numpy array in RGB format.

        :return: Float32 numpy array of dimension (336, 336, 3)
        :rtype: np.ndarray
        """
        image_path = (
            KVASIR_CAPSULE_PATH
            / findingclass_to_dirname(self.finding_class)
            / self.filename
        )
        image = Image.open(image_path).convert("RGB")
        image_arr = np.asarray(image, dtype=np.float32) / 255.0
        return image_arr
