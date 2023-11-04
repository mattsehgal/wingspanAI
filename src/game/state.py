from typing import Dict, List


class State:
    def __init__(self):
        pass


class BirdFeederState(State):
    def __init__(self, bird_feeder):
        self.in_dice: List[str] = [die.current_face for die in bird_feeder.dice_in]
        self.out_dice: List[str] = [die.current_face for die in bird_feeder.dice_out]


class BoardState(State):
    def __init__(self, board):
        self.player_id: int = board.player_id
        self.forest_state: Dict[int, Dict[str, int]] = board.forest.state
        self.grassland_state: Dict[int, Dict[str, int]] = board.grassland.state
        self.wetland_state: Dict[int, Dict[str, int]] = board.wetland.state

    def _get_bird_habitat_state(self, bird_id: int) -> Dict[int, Dict[str, int]]:
        return [habitat_state for habitat_state in zip(self.forest_state, self.grassland_state, self.wetland_state)
                if bird_id in habitat_state][0]

    def get_habitat_state(self, habitat: str) -> Dict[int, Dict[str, int]]:
        if habitat == 'forest':
            return self.forest_state
        elif habitat == 'grassland':
            return self.grassland_state
        elif habitat == 'wetland':
            return self.wetland_state

    def lay_eggs(self, bird_ids: List[int], egg_n: List[int]):
        for bird_id, n in zip(bird_ids, egg_n):
            habitat = self._get_bird_habitat_state(bird_id)
            habitat[bird_id]['eggs'] += n


class DeckState(State):
    def __init__(self, deck):
        self.tray = deck.tray


class PlayerState(State):
    def __init__(self, player):
        self.player_id: int = player.id
        self.bird_card_ids: List[int] = [bird_card.id for bird_card in player.bird_cards]
        self.bonus_card_ids: List[int] = [bonus_card.id for bonus_card in player.bonus_cards]
        self.food_tokens: Dict[str, int] = player.food_tokens
        self.board_state: BoardState = player.board.state

    def play_bird(self, bird_id: int, habitat: str, food_tokens: List[str], egg_bird_ids: List[int]):
        self.bird_card_ids.remove(bird_id)
        habitat_state = self.board_state.get_habitat_state(habitat)
        habitat_state[bird_id]
        # gets tricky here trying to add bird to habitat_state but not having access to BirdCard.state to update habitat_state with


class GameState(State):
    def __init__(self, game):
        self.current_player_id = game.current_player.id
        self.bird_feeder_state: BirdFeederState = BirdFeederState(game.bird_feeder)
        self.tray_state: DeckState = DeckState(game.bird_deck)
        self.player_states: Dict[int, PlayerState] = {player.id: PlayerState(player) for player in game.players}
        self.board_states: Dict[int, BoardState] = {player_id: state.board_state
                                                    for player_id, state in self.player_states.items()}

    def gain_from_birdfeeder(self, food_dice: List[str]):
        for die in food_dice:
            self.bird_feeder_state.in_dice.remove(die)
            self.bird_feeder_state.out_dice.append(die)

    def gain_from_supply(self, food_tokens: List[str]):
        for token in food_tokens:
            self.player_states[self.current_player_id].food_tokens[token] += 1




