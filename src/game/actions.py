

# Base Player Actions
class Action:
    def __init__(self, **kwargs):
        pass

    def execute(self, game):
        pass


class PlayBirdAction(Action):
    def __init__(self, **kwargs):
        pass

    def execute(self, game):
        player = game.current_player
        choice = game.get_player_input(type='play_bird')
        player.board.play_bird(choice)


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
        args = game.get_player_input()
        player.board.current_space.bird.cache(args)


class ComplexAction(Action):
    def execute(self, game):
        pass


class DiscardAction(Action):
    def execute(self, game):
        player = game.current_player
        args = game.get_player_input(type='discard')
        player.board.discard(args)


class DrawBonusAction(Action):
    def execute(self, game):
        player = game.current_player
        game.bonus_deck.draw()  # args from where?
        DiscardAction().execute(game)


class ExchangeAction(Action):
    def execute(self, game):
        player = game.current_player
        args = game.get_player_input(type='exchange')
        game.exchange(args)


class FlockingAction(Action):
    def execute(self, game):
        player = game.current_player
        args = game.get_player_input(type='flocking')
        player.board.current_space.bird.tuck(args)  # or something


class GiveToPlayerAction(Action):
    def execute(self, game):
        pass


class HuntingAction(Action):
    def execute(self, game):
        pass


class RepeatPowerAction(Action):
    def execute(self, game):
        pass

