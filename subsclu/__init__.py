"""Package of model using to cluster code submissions."""

import logging

from subsclu.model import SubmissionsClustering

__all__ = ["SubmissionsClustering"]

logging.getLogger(__name__).addHandler(logging.NullHandler())
