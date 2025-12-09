import os
from pathlib import Path
from typing import Any, List, Optional

import albumentations as A  # type: ignore[import-untyped]
from torch.utils.data import Dataset

from .config import KVASIR_CAPSULE_PATH
from .download import download_all
from .metadata import KvasirCapsuleMetadata
from .sample import KvasirCapsuleSample
from .split import PatientRatioSplit
from .transforms import kvasir_capsule_transforms
from .types import FindingClass, findingclass_to_dirname


class KvasirCapsuleSubset(Dataset):
    def __init__(
        self,
        phase: str,
        samples: List[KvasirCapsuleSample],
        transform: Optional[A.BaseCompose] = None,
    ):
        self.phase = phase
        self.samples: List[KvasirCapsuleSample] = samples
        self.transform = (
            kvasir_capsule_transforms.get(phase) if transform is None else transform
        )

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index) -> Any:
        sample: KvasirCapsuleSample = self.samples[index]
        image = sample.load_image()
        bboxes = sample.bbox.to_yolo() if sample.bbox else None
        class_labels = sample.finding_class.value
        if self.transform is not None:
            augmented = self.transform(
                image=image, bboxes=bboxes, class_labels=class_labels
            )
            return augmented["image"], augmented["bboxes"], augmented["class_labels"]
        else:
            return image, bboxes, class_labels


class KvasirCapsuleDataset:
    def __init__(
        self,
        split: Optional[PatientRatioSplit] = None,
        download: bool = True,
        path: Optional[Path] = None,
    ):
        super().__init__()
        self.path = KVASIR_CAPSULE_PATH if path is None else path

        if download:
            self.download(overwrite=False)
        if not self.exists(fail=True):
            raise RuntimeError(
                "Could not properly download or extract KvasirCapsule dataset."
            )
        self.metadata = KvasirCapsuleMetadata()
        if split is None:
            self.split = PatientRatioSplit(train=0.8, val=0.1, test=0.1)
            self.split.generate(self.metadata)
        else:
            self.split = split

    @property
    def train(self, transform: Optional[A.BaseCompose] = None) -> KvasirCapsuleSubset:
        samples = self.split.samples["train"]
        return KvasirCapsuleSubset("train", samples, transform)

    @property
    def val(self, transform: Optional[A.BaseCompose] = None) -> KvasirCapsuleSubset:
        samples = self.split.samples["val"]
        return KvasirCapsuleSubset("val", samples, transform)

    @property
    def test(self, transform: Optional[A.BaseCompose] = None) -> KvasirCapsuleSubset:
        samples = self.split.samples["test"]
        return KvasirCapsuleSubset("test", samples, transform)

    def exists(self, fail: bool = False) -> bool:
        """
        Check if dataset was already downloaded.

        Succeeds if metadata.csv is available and directories for all finding classes exist and are
        populated.

        :param fail: Whether to raise exceptions if data cannot be loaded, defaults to False
        :type fail: bool, optional
        :raises FileNotFoundError:
        :return: True if data can be loaded properly
        :rtype: bool
        """
        # check if kvasircapsule directory is there
        if not self.path.is_dir():
            if fail:
                raise FileNotFoundError(f"{self.path} is not a directory.")
            return False
        # check if metadata file exists
        metadata_path = self.path / "metadata.csv"
        if not metadata_path.is_file():
            if fail:
                raise FileNotFoundError(
                    f"Could not find metadata.csv in {metadata_path}."
                )
            return False
        # check if subdirectories for images exist
        subdirs_exist = [
            (self.path / findingclass_to_dirname(c)).is_dir() for c in FindingClass
        ]
        if not all(subdirs_exist):
            if fail:
                raise FileNotFoundError(
                    f"Incomplete class directories: {sum(subdirs_exist)} / {len(subdirs_exist)} available."
                )
            return False
        # check if subdirectories for images are populated
        subdirs_populated = [
            len(os.listdir(self.path / findingclass_to_dirname(c))) > 0
            for c in FindingClass
        ]
        if not all(subdirs_populated):
            if fail:
                raise FileNotFoundError("Image directory is not populated.")
            return False
        return True

    def download(self, overwrite: bool = False):
        # TODO implement proper overwrite with user prompt
        if self.exists() and not overwrite:
            return
        download_all()
