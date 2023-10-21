from board import Board


class Player:
    def __init__(self):
        self.hand = []
        self.board = Board()
        self.food_tokens = {'slug': 0,
                            'wheat': 0,
                            'berry': 0,
                            'fish': 0,
                            'rat': 0}
        self.eggs = 0
        self.score = 0

    def play_bird(self):
        pass

    def gain_food(self):
        pass

    def lay_eggs(self):
        pass

    def draw_bird_cards(self):
        pass

    def draw_bonus_cards(self):
        pass
