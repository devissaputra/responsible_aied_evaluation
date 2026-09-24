from collections.abc import Sequence


def demographic_parity_difference(predictions, groups, positive=1):
    """Return the maximum difference in positive prediction rate across groups."""
    if not predictions or len(predictions) != len(groups):
        raise ValueError("predictions and groups must be non-empty and have equal length")
    unique_groups = sorted(set(groups), key=str)
    rates = []
    for group in unique_groups:
        values = [prediction for prediction, label in zip(predictions, groups) if label == group]
        rates.append(sum(value == positive for value in values) / len(values))
    return max(rates) - min(rates) if rates else 0.0


def expected_calibration_error(
    probs: Sequence[float], outcomes: Sequence[int], bins: int = 10
) -> float:
    """Compute weighted absolute calibration error over equal width bins."""
    if not probs or len(probs) != len(outcomes):
        raise ValueError("probs and outcomes must be non-empty and have equal length")
    if bins <= 0:
        raise ValueError("bins must be positive")
    if any(not 0.0 <= value <= 1.0 for value in probs):
        raise ValueError("probabilities must be between 0 and 1")
    if any(value not in (0, 1) for value in outcomes):
        raise ValueError("outcomes must contain only 0 and 1")

    total = len(probs)
    error = 0.0
    for bin_index in range(bins):
        lower = bin_index / bins
        upper = (bin_index + 1) / bins
        members = [
            index
            for index, probability in enumerate(probs)
            if lower <= probability < upper
            or (bin_index == bins - 1 and probability == 1)
        ]
        if members:
            confidence = sum(probs[i] for i in members) / len(members)
            accuracy = sum(outcomes[i] for i in members) / len(members)
            error += len(members) / total * abs(confidence - accuracy)
    return error


def deployment_gate(ece, fairness_gap, privacy_reviewed, human_oversight):
    """Apply explicit minimum governance checks before a hypothetical deployment."""
    if not 0.0 <= ece <= 1.0 or not 0.0 <= fairness_gap <= 1.0:
        raise ValueError("ece and fairness_gap must be between 0 and 1")
    return (
        ece <= 0.10
        and fairness_gap <= 0.10
        and bool(privacy_reviewed)
        and bool(human_oversight)
    )
