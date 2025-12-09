#!/usr/bin/env python3
from pathlib import Path

import click

from kvasircapsuleloader import KvasirCapsuleDataset


@click.command()
def main():
    dataset = KvasirCapsuleDataset()
    out_path = Path("splits/default_80_10_10.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dataset.split.save(out_path)


if __name__ == "__main__":
    main()
