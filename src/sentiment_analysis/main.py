from pathlib import Path

import polars as pl
from tqdm import tqdm

from sentiment_analysis.core.filter import Filter
from sentiment_analysis.extension.commit_filters import Contains, Length

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[2]
    data_dir = base_dir / "data"

    csv_path = data_dir / "csv" / "dhruvildave_github-commit-messages-dataset.csv"
    target_col = "message"

    filters: list[Filter] = [
        Length(target_col, 0, 14),
        ~Length(target_col, 0, 14),
        Length(target_col, 15, 72),
        Contains(target_col, "test"),
    ]

    for i, f in enumerate(tqdm(filters, desc="Processing masks"), start=1):
        export_path = data_dir / "csv" / f"mask_{i}_{f.name}.csv"
        (
            pl.scan_csv(csv_path, infer_schema_length=0, encoding="utf8")
            .filter(f())
            .select(target_col)
            .sink_csv(export_path)
        )
