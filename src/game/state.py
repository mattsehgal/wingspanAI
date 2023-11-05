from typing import Dict, List


class State:
    def __init__(self):
        pass


class BirdState(State):
    def __init__(self, bird_id: int, color: str, eggs: int, habitat: Dict[str, bool]):
        self.bird_id = bird_id
        self.color = color
        self.eggs = eggs
        self.habitat = habitat

    def __eq__(self) -> int:
        return self.bird_id


class HabitatState(State):
    def __init__(self, habitat: str, bird_states: List[BirdState]):
        self.habitat = habitat
        self.bird_states = bird_states
        self.id_state_map = {state.id: state for state in self.bird_states}

    def play_bird(self, bird_id: int, bird_id_egg_n: Dict[int, int]):
        pass

    def lay_eggs(self, bird_id_egg_n: Dict[int, int]):
        for bird_id, egg_n in bird_id_egg_n.items():
            bird_state = self.id_state_map[bird_id]
            bird_state.eggs += egg_n


class BoardState(State):
    def __init__(self, player_id: int, habitat_states: Dict[str, HabitatState]):
        self.player_id = player_id
        self.forest_state = habitat_states['forest']
        self.grassland_state = habitat_states['grassland']
        self.wetland_state = habitat_states['wetland']

    def _get_bird_habitat_state(self, bird_id: int) -> HabitatState:
        return [habitat_state for habitat_state in [self.forest_state,
                                                    self.grassland_state,
                                                    self.wetland_state]
                if bird_id in habitat_state.bird_states][0]

    def get_habitat_state(self, habitat: str) -> HabitatState:
        if habitat == 'forest':
            return self.forest_state
        elif habitat == 'grassland':
            return self.grassland_state
        elif habitat == 'wetland':
            return self.wetland_state


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


class BirdFeederState(State):
    def __init__(self, bird_feeder):
        self.in_dice: List[str] = [die.current_face for die in bird_feeder.dice_in]
        self.out_dice: List[str] = [die.current_face for die in bird_feeder.dice_out]


class GameState(State):
    def __init__(self,
                 curr_player_id: int,
                 component_states: Dict[str, State],
                 player_states: Dict[int, PlayerState]):
        self.current_player_id = curr_player_id
        self.bird_feeder_state: BirdFeederState = component_states['bird_feeder']
        self.tray_state: DeckState = component_states['bird_deck']
        self.player_states = player_states
        self.board_states: Dict[int, BoardState] = {player_id: state.board_state
                                                    for player_id, state in self.player_states.items()}

    def gain_from_birdfeeder(self, food_dice: List[str]):
        for die in food_dice:
            self.bird_feeder_state.in_dice.remove(die)
            self.bird_feeder_state.out_dice.append(die)

    def gain_from_supply(self, food_tokens: List[str]):
        for token in food_tokens:
            self.player_states[self.current_player_id].food_tokens[token] += 1

