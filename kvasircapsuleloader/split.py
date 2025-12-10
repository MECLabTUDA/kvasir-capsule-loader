import itertools
import json
import logging
from pathlib import Path
from typing import Dict, List, Literal

import numpy as np

from .config import DEFAULT_RANDOM_SEED
from .metadata import KvasirCapsuleMetadata
from .sample import KvasirCapsuleSample
from .utils import fix_random_seed


class PatientRatioSplit:
    """
    Generalized split by ratio that respects patient IDs (Experimental)
    """

    def __init__(self, **ratios):
        """
        :raises ValueError: If ratios don't add up to 1.0
        """
        if sum(list(ratios.values())) != 1.0:
            raise ValueError("Split ratios need to sum up to 1.")
        self._ratios = ratios

    def generate(
        self,
        metadata: KvasirCapsuleMetadata,
        strategy: Literal["shuffle", "sort"] = "sort",
        seed: int = DEFAULT_RANDOM_SEED,
    ):
        """
        Generate sample assignments for the split.

        :param metadata: _description_
        :type metadata: KvasirCapsuleMetadata
        :param strategy: _description_, defaults to "sort"
        :type strategy: Literal[&quot;shuffle&quot;, &quot;sort&quot;], optional
        :param seed: _description_, defaults to DEFAULT_RANDOM_SEED
        :type seed: int, optional
        """
        self._seed = seed
        self.samples: Dict[str, List[KvasirCapsuleSample]] = {
            key: [] for key in self._ratios
        }
        fix_random_seed(self._seed)
        S = metadata.samples_by_class_by_patient()
        for finding_class, patient_dict in S.items():
            patients = list(patient_dict.values())
            N_patients = len(patients)
            if N_patients < len(self._ratios):
                logging.warning(
                    f"Could not split finding class {finding_class}: "
                    f"Too few patients {N_patients}, should be {len(self._ratios)} or more."
                )
                logging.warning(f"Ignoring class {finding_class}.")
                continue

            first_phase = list(self._ratios.keys())[0]
            N = {
                first_phase: N_patients
            }
            # make sure that sets represent at least one patient
            for phase, ratio in self._ratios.items():
                if phase == first_phase:
                    continue
                N[phase] = max(int(np.round(N_patients * ratio)), 1)
                N[first_phase] -= N[phase]
            assert N[first_phase] > 0
            idx = np.arange(N_patients)
            if strategy == "sort":
                # sort indices descending by number of samples
                # --> first set will contain most samples
                idx = np.argsort([len(p) for p in patients])[::-1]
            else:
                np.random.shuffle(idx)
            pointer = 0
            for phase, ratio in self._ratios.items():
                sub_idx = idx[pointer : pointer + N[phase]]
                self.samples[phase].extend(
                    list(itertools.chain.from_iterable([patients[i] for i in sub_idx]))
                )
                pointer += N[phase]

    @staticmethod
    def load(path: Path, metadata: KvasirCapsuleMetadata) -> "PatientRatioSplit":
        """
        Load split definition from JSON.

        Requires an instantiated KvasirCapsuleMetadata object that can be obtained
        simply by constructing it.

        :param path: Path to input JSON file.
        :type path: Path
        :param metadata: KvasirCapsuleMetadata object.
        :type metadata: KvasirCapsuleMetadata
        :return: Populated PatientRatioSplit object
        :rtype: PatientRatioSplit
        """
        with open(path, "r") as f:
            data = json.load(f)
        split = PatientRatioSplit(
            **data["ratios"]
        )
        split._seed = data["seed"]
        S = metadata.samples_by_filename()
        for phase in split._ratios:
            split.samples[phase] = [S[filename] for filename in data["samples"][phase]]
        return split

    def save(self, path: Path):
        """
        Save split definition to JSON.

        :param path: Path to output JSON. Parent directories must exist.
        :type path: Path
        """
        data = {
            "ratios": {**self._ratios},
            "seed": self._seed,
            "samples": {
                phase: [sample.filename for sample in self.samples[phase]]
                for phase in self._ratios
            },
        }
        with open(path, "w") as f:
            json.dump(data, f)


def make_kfold_split(k: int):
    assert k > 0
    return PatientRatioSplit(
        **{ f"fold{i}": 1 / k for i in range(k) }
    )
