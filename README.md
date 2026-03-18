<div align="center">
    <img src="https://img.icons8.com/ios-glyphs/100/7AB696/speech-bubble-with-dots.png" alt="speech-bubble-with-dots" />
    <h2>Semantic Analysis Study</h2>
    <p><b>GitHub Commit Messages Quality Model</b></p>
    <p align="justify">Originally developed during <a href="https://unihack2026.devpost.com/">UNIHACK 2026</a> as part of the <a href="https://devpost.com/software/github-ranked-vqk476">GitRank</a> project, where commit message quality was used as a contributing factor in ELO score calculation. This repository extracts and refines that logic beyond the 48-hour hackathon constraint.</p>
</div>

---

<h3 align="center">Quality Criteria</h3>

Commit message quality is assessed against these references:
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Chris Beams' Seven Rules](https://cbea.ms/git-commit/).

The operative criteria for automated scoring are subject line length (50–72 chars), imperative mood, and the presence of a valid `type(scope):` prefix.

> Imperative mood is the most difficult criterion to assess programmatically. In practice this is approximated by screening for unprofessional or emotionally charged language that would disrupt the tone of a commit history, rather than strict grammatical analysis.

<h3 align="center">Current Progress</h3>

Components currently built and in active use.

- Added `Filter`- Composable wrapper around `pl.Expr` for efficiently masking and extracting subsets of large CSVs via Polars lazy evaluation.
- Added `Encoder` - Wrapper around `SentenceTransformer` for encoding raw text and CSV columns into embeddings. ONNX optimisation planned for more lightweight workflows.

<h3 align="center">Additional Notes</h3>

Ideas and tooling evaluated for potential extension scenarios.

- `FAISS` was used during the hackathon to rapidly retrieve semantically similar entries against positive and negative examples, bypassing the need for exhaustive comparison under time pressure. Retained for similarity search experiments.
- `UMAP` was used for dimension reduction on high-dimensional embeddings prior to fitting `IsolationForest` and `OneClassSVM` models, both of which degrade in high dimensions.