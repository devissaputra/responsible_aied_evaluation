# Data Policy

The research bundle retrieves real UCI dataset 697 at run time using `ucimlrepo`.

Raw learner-level source data are not committed.

The empirical adapter records:

- UCI dataset ID and DOI;
- original source target counts;
- normalized dataset SHA-256 fingerprint;
- post-enrollment features excluded;
- audit-only attributes excluded from prediction;
- runtime package versions.

The fingerprint is computed over the retrieved feature matrix plus original target in row/column order.

See:

- ../DATA.md for provenance and endpoint semantics;
- ../docs/dataset_card.md for the population and target transformation;
- ../docs/research_protocol.md for the frozen analysis design;
- ../REPRODUCIBILITY.md for execution details.
