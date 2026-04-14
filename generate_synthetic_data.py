"""Generate synthetic e-commerce product datasets for sorting experiments.

Run this file directly. It will generate a fixed set of synthetic datasets
without requiring any terminal arguments.
"""

import csv
import json
import random
from pathlib import Path


SIZES = [100, 500, 1000, 5000, 10000]
OUTPUT_DIR = Path("synthetic_datasets")
SEED = 42
MIN_PRICE = 10
MAX_PRICE = 100000
START_PRODUCT_ID = 1000


def generate_dataset(size, rng, start_product_id, min_price, max_price):
    """Generate a single synthetic product dataset."""
    dataset = []
    for index in range(size):
        dataset.append((start_product_id + index, rng.randint(min_price, max_price)))
    return dataset


def write_csv(path, dataset):
    """Write a dataset to CSV."""
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["Product_ID", "Price_ETB"])
        writer.writerows(dataset)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rng = random.Random(SEED)
    manifest = {
        "seed": SEED,
        "min_price": MIN_PRICE,
        "max_price": MAX_PRICE,
        "start_product_id": START_PRODUCT_ID,
        "datasets": [],
    }

    current_product_id = START_PRODUCT_ID
    for size in SIZES:
        dataset = generate_dataset(size, rng, current_product_id, MIN_PRICE, MAX_PRICE)
        current_product_id += size

        file_path = OUTPUT_DIR / f"products_{size}.csv"
        write_csv(file_path, dataset)

        manifest["datasets"].append(
            {
                "size": size,
                "file": file_path.name,
                "first_record": dataset[0] if dataset else None,
                "last_record": dataset[-1] if dataset else None,
            }
        )

        print(f"Generated {size:,} records -> {file_path}")

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Manifest written -> {manifest_path}")


if __name__ == "__main__":
    main()