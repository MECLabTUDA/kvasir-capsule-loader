from typing import Dict, List, Optional

import pandas as pd

from .bbox import BoundingBox
from .config import KVASIR_CAPSULE_PATH
from .sample import KvasirCapsuleSample
from .types import FindingClass, str_to_findingcategory, str_to_findingclass


class KvasirCapsuleMetadata:
    """
    This is basically an abstraction for the records in metadata.csv.
    """

    def __init__(self) -> None:
        self._data = pd.read_csv(KVASIR_CAPSULE_PATH / "metadata.csv", delimiter=";")
        self.video_ids = self._data.video_id
        self.samples: List[KvasirCapsuleSample] = []
        self._load_samples()

    def _load_samples(self):
        """
        Load KvasirCapsuleSample instances from metadata.csv file.
        """
        for i, row in self._data.iterrows():
            finding_category = str_to_findingcategory(row.finding_category)
            finding_class = str_to_findingclass(row.finding_class)
            if None in (row[["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"]]):
                bbox = None
            else:
                bbox = BoundingBox.from_kvasir_capsule(
                    row.x1,
                    row.y1,
                    row.x2,
                    row.y2,
                    row.x3,
                    row.y3,
                    row.x4,
                    row.y4,
                )
            sample = KvasirCapsuleSample(
                row.filename,
                row.video_id,
                row.frame_number,
                finding_category,
                finding_class,
                bbox,
            )
            self.samples.append(sample)

    def samples_by_filename(self) -> Dict[str, KvasirCapsuleSample]:
        """
        Return dict of samples, accessible by sample filename.

        :return: Mapping of sample filenames to corresponding KvasirCapsuleSample
        :rtype: Dict[str, KvasirCapsuleSample]
        """
        # TODO cache
        return {sample.filename: sample for sample in self.samples}

    def samples_by_class_by_patient(
        self,
    ) -> Dict[FindingClass, Dict[str, List[KvasirCapsuleSample]]]:
        """
        Return a dict that can be accessed sample=d[finding_class][video_id].
        Useful for data splitting by patient id.

        :return: _description_
        :rtype: Dict[FindingClass, Dict[str, List[KvasirCapsuleSample]]]
        """
        # TODO cache
        S: Dict[FindingClass, Dict[str, List[KvasirCapsuleSample]]] = {}
        for sample in self.samples:
            if sample.finding_class not in S:
                S[sample.finding_class] = {}
            if sample.video_id not in S[sample.finding_class]:
                S[sample.finding_class][sample.video_id] = []
            S[sample.finding_class][sample.video_id].append(sample)
        return S

    def num_patients(self) -> int:
        """
        Return total number of patients.

        :return: Number of patients
        :rtype: int
        """
        return len(self.video_ids.unique())

    def num_samples(self) -> int:
        """
        Return total number of samples (images)

        :return: Number of samples (images)
        :rtype: int
        """
        return len(self.samples)

    def filter(
        self,
        include: Optional[List[FindingClass]] = None,
        exclude: Optional[List[FindingClass]] = None,
    ) -> "KvasirCapsuleMetadata":
        # TODO implement
        raise NotImplementedError()
