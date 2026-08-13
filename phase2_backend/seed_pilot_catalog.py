"""Command-line entrypoint for the review-only pilot catalog seed."""

from __future__ import annotations

import argparse
import os

from phase2_backend.commerce.database import CommerceSessionLocal
from phase2_backend.commerce.pilot_catalog_seed import PilotCatalogSeeder


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preview or apply the non-sellable CropPulse pilot draft catalog.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Commit the draft records. Without this flag all changes are rolled back.",
    )
    parser.add_argument(
        "--allow-production",
        action="store_true",
        help="Explicitly permit execution when ENV is production.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    environment = os.getenv("ENV", "development").strip().lower()
    if environment in {"production", "prod"} and not args.allow_production:
        raise SystemExit("Refusing to seed production without --allow-production and an approved change plan.")

    with CommerceSessionLocal() as session:
        result = PilotCatalogSeeder(session).seed(apply=args.apply)

    mode = "applied" if result.applied else "previewed and rolled back"
    print(
        f"Pilot draft catalog {mode}: {result.categories} categories, "
        f"{result.products} products, {result.skus} SKUs, {result.prices} prices."
    )
    if result.applied:
        print("All seeded categories, products, SKUs, and price lists remain inactive/draft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
