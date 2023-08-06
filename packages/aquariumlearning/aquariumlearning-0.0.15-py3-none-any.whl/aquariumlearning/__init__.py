# Only expose public API
from .client import (
    Client,
    LabeledDataset,
    LabeledFrame,
    Inferences,
    InferencesFrame,
    LabelClassMap,
    ClassMapEntry,
    CustomMetricsDefinition,
    viridis_rgb,
)

from .issues import IssueManager, Issue, IssueElement


# TODO: Avoid duplicating here while still getting nice autodoc?
__all__ = [
    "Client",
    "LabeledDataset",
    "LabeledFrame",
    "Inferences",
    "InferencesFrame",
    "LabelClassMap",
    "ClassMapEntry",
    "CustomMetricsDefinition",
    "viridis_rgb",
    "IssueManager",
    "Issue",
    "IssueElement",
]
