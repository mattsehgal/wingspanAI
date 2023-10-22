

class Action:
    def __init__(self, n):
        self.n = n


class PlayBirdAction(Action):
    def execute(self):
        pass


class GainFoodAction(Action):
    def __init__(self):
        pass


class LayEggsAction(Action):
    def __init__(self):
        pass


class DrawCardsAction(Action):
    def __init__(self):
        pass


class ExchangeAction(Action):
    def __init__(self):
        pass
