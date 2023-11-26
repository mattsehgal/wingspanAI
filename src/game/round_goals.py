from typing import Any, Callable, Dict, List

"""
Eggs in forest, prairie, and wetland habitats

Birds in forest, prairie, and wetland habitats

Brown birds, white/no power birds

Total eggs in each of four nest types: cup, cavity, ground, and platform

Birds with at least one egg in each of four nest types: cup, cavity, ground, and platform

Birds with no eggs

Birds worth equal or less than 3 points; birds worth more than 4 points

Food in personal supply; cards in hand

Sets of eggs in all three habitats

Filled columns

Birds in a row

Total Birds

Beaks point left and right

Cubes on "play a bird"

Birds with tucked cards

Food cost of played birds

In food cost of your birds: worms; berries and seeds; fish and rats

No goal
"""


class RoundGoal:
    def __init__(self, func: Callable):
        self.func = func
        self.ranking = []

    def calculate(self, game_state: "GameState"):
        self.ranking = self.func(game_state)


class RoundGoalFactory:
    def __init__(self):
        pass

    @staticmethod
    def _birds_in_habitat(habitat: str):
        def func(game_state: "GameState"):
            ids_birds = [(_id, len(board.habitats[habitat].birds)) for _id, board
                         in game_state.player_boards.items()]
            sorted_ids_birds = sorted(ids_birds, key=lambda x: x[1], reverse=True)
            return [item[0] for item in sorted_ids_birds]
        return RoundGoal(func)

    @staticmethod
    def _eggs_in_habitat(habitat: str) -> RoundGoal:
        def func(game_state: "GameState"):
            ids_eggs = [(_id, board.habitats[habitat].eggs()) for _id, board
                        in game_state.player_boards.items()]
            sorted_ids_eggs = sorted(ids_eggs, key=lambda x: x[1], reverse=True)
            return [item[0] for item in sorted_ids_eggs]
        return RoundGoal(func)

    def create(self, args: Dict[str, str]) -> RoundGoal:
        rg_type = args['type']
        if 'IN_HABITAT' in rg_type:
            habitat = args['habitat']
            if 'BIRDS' in rg_type:
                return self._birds_in_habitat(habitat)
            elif 'EGGS' in rg_type:
                return self._eggs_in_habitat(habitat)


class RoundGoalsBoard:
    def __init__(self):
        self.round_goals = []
        self.round_number = 1
        self.rounds = 4

    def calculate(self, game_state: "GameState") -> List[int]:
        if self.round_number <= self.rounds:
            round_goal = self.round_goals[self.round_number - 1]
            round_goal.calculate(game_state)
            return round_goal.ranking

        return []
