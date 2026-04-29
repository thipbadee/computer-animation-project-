class ExponentialAngleFilter:
    """Simple EMA smoother for noisy pose-derived angles."""

    def __init__(self, alpha: float = 0.35):
        self.alpha = alpha
        self.value = None

    def reset(self):
        self.value = None

    def update(self, measurement: float | None) -> float | None:
        if measurement is None:
            return self.value
        if self.value is None:
            self.value = measurement
        else:
            self.value = (self.alpha * measurement) + ((1.0 - self.alpha) * self.value)
        return self.value
