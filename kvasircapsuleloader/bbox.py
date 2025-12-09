import numpy as np


class BoundingBox:
    """
    Canonical Bounding Box class that supports conversion from and to several
    formats, such as Yolo or Pascal VOC.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.norm_x = 1
        self.norm_y = 1

    @staticmethod
    def from_pascal_voc(
        x_min: int,
        y_min: int,
        x_max: int,
        y_max: int,
        image_width: int,
        image_height: int,
    ) -> "BoundingBox":
        assert x_min <= x_max
        assert y_min <= y_max
        bbox = BoundingBox()
        bbox.x = x_min
        bbox.y = y_min
        bbox.width = x_max - x_min
        bbox.height = y_max - y_min
        bbox.norm_x = image_width
        bbox.norm_y = image_height
        return bbox

    @staticmethod
    def from_yolo(
        x_center_n: float,
        y_center_n: float,
        width_n: float,
        height_n: float,
        image_width: int,
        image_height: int,
    ) -> "BoundingBox":
        bbox = BoundingBox()
        bbox.width = int(np.round(width_n * image_width))
        bbox.height = int(np.round(height_n * image_height))
        bbox.norm_x = image_width
        bbox.norm_y = image_height
        bbox.x = int(np.round((x_center_n - width_n / 2) * image_width))
        bbox.y = int(np.round((y_center_n - height_n / 2) * image_height))
        return bbox

    @staticmethod
    def from_kvasir_capsule(
        x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int
    ) -> "BoundingBox":
        bbox = BoundingBox()
        bbox.x = min(x1, x2, x3, x4)
        bbox.y = min(y1, y2, y3, y4)
        bbox.width = max(x1, x2, x3, x4) - bbox.x
        bbox.height = max(y1, y2, y3, y4) - bbox.y
        bbox.norm_x = 336
        bbox.norm_y = 336
        return bbox

    def to_yolo(self) -> np.ndarray:
        """
        Return numpy array in YOLO format (x_center_n, y_center_n, width_n, height_n).

        :return: Array of four float32s (x_center_n, y_center_n, width_n, height_n)
        :rtype: np.ndarray
        """
        return np.array(
            [
                (self.x + self.width / 2) / self.norm_x,
                (self.y + self.height / 2) / self.norm_y,
                self.width / self.norm_x,
                self.height / self.norm_y,
            ],
            dtype=np.float32,
        )

    def to_pascal_voc(self) -> np.ndarray:
        """
        Return numpy array in Pascal VOC format (x_min, y_min, x_max, y_max).

        :return: Array of four ints (x_min, y_min, x_max, y_max)
        :rtype: np.ndarray
        """
        return np.array([self.x, self.y, self.x + self.width, self.y + self.height])
