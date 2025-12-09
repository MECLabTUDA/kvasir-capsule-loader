# KvasirCapsule Loader

An inofficial abstraction for the KvasirCapsule dataset that aims to provide the following features:

* **Convenient abstraction** for KvasirCapsule as a Pytorch Dataset with augmentations
* **Patient-separating dataset splits** that are truely separate and reproducible
* **Auto-download** KvasirCapsule dataset
* **Canonical representation** of finding categories, finding classes, folder structures and bounding boxes
* **Unit tests**, type hints for type checking and error handling


## Rationale

**Convenience**: Loading a dataset for an experiment should be as simple as issuing a single function call.

**Proper Data Splits**: The KvasirCapsule dataset itself features an official two-fold split.
However, this split seems to have [patient overlap](https://github.com/simula/kvasir-capsule/issues/2), which may lead to overfitting when used in a training setup.
Further, a two-fold split is not enough for a training/validation/test setup, k-fold cross-validation, or out-of-distribution detection.

**Modern Python tooling**: Enables a smooth workflow and up-to-date dependencies.

**Error and type checking**: Canonical representations of classes, categories and bounding boxes as dedicated types allow for proper error handling and avoid common pitfalls in data processing pipelines.

## Getting Started

The latest release of this project can be installed through pip:

```bash
pip install kvasircapsuleloader
```

Once installed, including KvasirCapsule as a pytorch dataset is as simple as running:

```python
...
from kvasircapsuleloader import KvasirCapsuleDataset

dataset = KvasirCapsuleDataset()
dataloader_train = DataLoader(dataset.train())
dataloader_val = DataLoader(dataset.val())
dataloader_test = DataLoader(dataset.test())
```

Please note that this call will automatically download the KvasirCapsule dataset from the OSF repo if it is not available yet.


## Roadmap

TODOs:

* [ ] Splits for k-fold cross-validation
* [ ] Splits for OOD-detection (held-out training set)
* [ ] Visualization utilities
* [ ] Allow user to select only samples with bounding boxes
* [ ] Selection criteria, only include selected classes


## Acknowledgement

This project provides an abstraction for the [KvasirCapsule Dataset](https://osf.io/preprints/osf/gr7bn_v1) by Smedsrud et al., which is licensed under CC-BY-SA 4.0.
Please refer to the [Kvasir Capsule GitHub Repository](https://github.com/simula/kvasir-capsule) for terms of use and the corresponding BibTeX entry.