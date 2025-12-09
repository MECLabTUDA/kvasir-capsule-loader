import albumentations as A  # type: ignore[import-untyped]
from albumentations.pytorch import ToTensorV2  # type: ignore[import-untyped]

_T_train = A.Compose(
    [
        A.ColorJitter(),
        A.Resize(224, 224),
        A.RandomRotate90(),
        A.HorizontalFlip(),
        A.Normalize((0.5,), (0.225,)),
        ToTensorV2(),
    ],
    bbox_params=A.BboxParams(format="yolo"),
)
_T_val = A.Compose(
    [
        A.Resize(224, 224),
        A.Normalize((0.5,), (0.225,)),
        ToTensorV2(),
    ]
)
_T_test = _T_val

kvasir_capsule_transforms = {"train": _T_train, "val": _T_val, "test": _T_test}
