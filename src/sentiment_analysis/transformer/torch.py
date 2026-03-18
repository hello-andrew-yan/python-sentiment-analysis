from dataclasses import dataclass, field
from pathlib import Path

import polars as pl
import torch
from sentence_transformers import SentenceTransformer


@dataclass
class EncoderConfig:
    model_id: str = "sentence-transformers/all-MiniLM-L6-v2"
    device: str = field(
        default_factory=lambda: "cuda" if torch.cuda.is_available() else "cpu"
    )


class Encoder:
    def __init__(self, config: EncoderConfig | None = None) -> None:
        self.config = config or EncoderConfig()
        self.model = SentenceTransformer(
            self.config.model_id,
            device=self.config.device,
            model_kwargs={
                "dtype": torch.float16
                if self.config.device == "cuda"
                else torch.float32
            },
        )

    def encode(
        self,
        texts: str | list[str],
        batch_size: int = 1024,
        show_progress_bar: bool = False,
        normalize: bool = True,
    ) -> torch.Tensor:
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            convert_to_tensor=True,
            device=self.config.device,
            normalize_embeddings=normalize,
        )

    def encode_csv_column(
        self, csv_path: Path, target_col: str, **kwargs
    ) -> torch.Tensor:
        kwargs.pop("texts", None)
        series = (
            pl.scan_csv(csv_path, infer_schema_length=0)
            .select(target_col)
            .collect()
            .get_column(target_col)
            .fill_null("")
        )
        return self.encode(texts=series.to_list(), **kwargs)
