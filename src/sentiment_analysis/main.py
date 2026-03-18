from pathlib import Path

import polars as pl
from tqdm import tqdm

from sentiment_analysis.core.filter import Filter
from sentiment_analysis.extension.commit import Length, Matches


def apply_masks(
    csv_path: Path,
    output_dir: Path,
    filters: list[Filter],
    export_cols: list[str] | str,
) -> None:
    for i, f in enumerate(tqdm(filters, desc="Processing masks"), start=1):
        export_path = output_dir / f"mask_{i}_{f.name}.csv"
        (
            pl.scan_csv(csv_path, infer_schema_length=0, encoding="utf8")
            .filter(f())
            .select(export_cols)
            .sink_csv(export_path)
        )


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[2]
    csv_dir = base_dir / "data" / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)

    csv_path = csv_dir / "dhruvildave_github-commit-messages-dataset.csv"
    filters: list[Filter] = [
        Matches("message", pattern=r"^\w+(\([^)]*\))?:\s*.+")
        & Length("message", 10, 72),
    ]

    apply_masks(csv_path, output_dir=csv_dir, filters=filters, export_cols="message")
