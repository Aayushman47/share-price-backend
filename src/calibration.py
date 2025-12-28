import numpy as np
from sklearn.isotonic import IsotonicRegression

class ConfidenceCalibrator:
    def __init__(self):
        self.model = IsotonicRegression(out_of_bounds="clip")
        self.fitted = False

    def fit(self, confidences, outcomes):
        """
        confidences: raw confidence values (0–1)
        outcomes: 1 if correct, 0 if incorrect
        """
        self.model.fit(confidences, outcomes)
        self.fitted = True

    def transform(self, confidences):
        if not self.fitted:
            raise RuntimeError("Calibrator not fitted")
        return self.model.transform(confidences)
