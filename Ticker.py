class Ticker:
    def __init__(self):
        self.counter = -1
    def __call__(self):
        self.counter += 1
        return self.counter

