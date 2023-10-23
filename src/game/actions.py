

# Base Player Actions
class Action:
    def execute(self, game):
        pass


class PlayBirdAction(Action):
    def execute(self, game):
        player = game.current_player
        # args = game.get_player_input(type='play_bird')
        # player.board.play_bird(args)


class GainFoodAction(Action):
    def execute(self, game):
        player = game.current_player
        # args = game.get_player_input(type='gain_food')
        # player.board.gain_food(args)


class LayEggsAction(Action):
    def execute(self, game):
        # see above
        pass


class DrawCardsAction(Action):
    def execute(self, game):
        # see above
        pass


# Other Actions
class CacheFoodAction(Action):
    def execute(self, game):
        player = game.current_player
        # hmm


class ComplexAction(Action):
    def execute(self, game):
        pass


class DiscardAction(Action):
    def execute(self, game):
        pass


class DrawBonusAction(Action):
    def execute(self, game):
        pass


class ExchangeAction(Action):
    def execute(self, game):
        pass


class FlockingAction(Action):
    def execute(self, game):
        pass


class GiveToPlayerAction(Action):
    def execute(self, game):
        pass


class HuntingAction(Action):
    def execute(self, game):
        pass


class RepeatPowerAction(Action):
    def execute(self, game):
        pass

