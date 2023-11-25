from src.game.actions import Action, ActionSequence
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


class RoundGoal(Action):
    def __init__(self):
        pass


class RoundGoalsBoard:
    def __init__(self):
        self.round_goals = []