from enum import Enum, auto

from typing import List


class StringEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.name


class ComponentType(StringEnum):
    ACTION = auto()
    ASSERTION = auto()
    CONDITION = auto()
    ELSE = auto()
    END_GROUP = auto()
    ENTAILMENT = auto()
    GROUP = auto()
    IF = auto()
    IF_WS = auto()
    ITEM = auto()
    LOCATION = auto()
    N = auto()
    ON = auto()
    OPTIONAL = auto()
    OR = auto()
    POWER = auto()
    PLAYERS = auto()
    WHEN = auto()
    WHEN_COND = auto()


class ComponentRegex(Enum):
    ACTION = r'(?P<ACTION>PLAY|GAINS?|LAYS?|DRAW|CACHE|DISCARD|KEEP|LOOK AT|MOVE|REPEAT|ROLL|TRADE|TUCK)'
    ASSERTION = r'\.$'
    CONDITION = r'(?P<CONDITION>ARE .+?,?|AT .+?|IF THEY .+?|PAY .+?|STARTING .+?|WITH (THE )?.+?:?)'
    ELSE = r'IF NOT,'
    END_GROUP = r')'
    ENTAILMENT = r'(?P<ENTAILMENT>\s?(ALSO|AND|TO|IF YOU DO,( ALSO)?|YOU MAY)\s?)'
    GROUP = r'('
    IF = r'(?P<IF>IF)'
    IF_WS = r'IF (?P<IF_WS>(\<|\>)\d+CM,)'
    ITEM = r'(?P<ITEM>(FACE-UP )?(?:\[.+?\]|BIRD|DICE|IT|NEW BONUS CARDS?))\.?'
    LOCATION = r'(\s?(?P<LOCATION>(?:NOT\s)?(?:BEHIND|FROM|(THAT ARE )?IN|ON|(IS )?TO|UNDER)\s?.+?)\.?)'
    N = r'(?P<N>(?:\d+|A( \w+)?|ALL|ANY( \d+)?|FOR ANY OTHER|THIS|THE \d+|\s))'
    ON = r'ON'
    OPTIONAL = r'?'
    OR = r'|'
    POWER = r'(?P<POWER>BROWN|PINK|PREDATOR|WHITE|\[.+?\])( POWER)?'
    PLAYERS = r'(?P<PLAYERS>PLAYER\(S\)|\w+)( PLAYER\'?S?)?'
    WHEN = r'(?P<WHEN>WHEN)'
    WHEN_COND = r'(?P<WHEN_COND>TAKES THE \"(.+?)\" ACTION|PLAYS A \[.+?\] BIRD|PREDATOR SUCCEEDS),?'


class ComponentMapper:
    _MAPPING = {
        ComponentType.ACTION:       ComponentRegex.ACTION,
        ComponentType.ASSERTION:    ComponentRegex.ASSERTION,
        ComponentType.CONDITION:    ComponentRegex.CONDITION,
        ComponentType.ELSE:         ComponentRegex.ELSE,
        ComponentType.END_GROUP:    ComponentRegex.END_GROUP,
        ComponentType.ENTAILMENT:   ComponentRegex.ENTAILMENT,
        ComponentType.GROUP:        ComponentRegex.GROUP,
        ComponentType.IF:           ComponentRegex.IF,
        ComponentType.IF_WS:        ComponentRegex.IF_WS,
        ComponentType.ITEM:         ComponentRegex.ITEM,
        ComponentType.LOCATION:     ComponentRegex.LOCATION,
        ComponentType.N:            ComponentRegex.N,
        ComponentType.ON:           ComponentRegex.ON,
        ComponentType.OPTIONAL:     ComponentRegex.OPTIONAL,
        ComponentType.OR:           ComponentRegex.OR,
        ComponentType.POWER:        ComponentRegex.POWER,
        ComponentType.PLAYERS:      ComponentRegex.PLAYERS,
        ComponentType.WHEN:         ComponentRegex.WHEN,
        ComponentType.WHEN_COND:    ComponentRegex.WHEN_COND,
    }

    _INVERSE = {v: k for k, v in _MAPPING.items()}

    @classmethod
    def get_regex(cls, component_type: ComponentType) -> ComponentRegex:
        return cls._MAPPING.get(component_type, None)

    @classmethod
    def get_type(cls, component_regex: ComponentRegex) -> ComponentType:
        return cls._INVERSE.get(component_regex, None)


class PowerType(StringEnum):
    ALL = auto()
    DISCARD = auto()
    DRAW = auto()
    EACH = auto()
    GAIN = auto()
    IF = auto()
    LAY = auto()
    LOOK = auto()
    PLAY = auto()
    PLAYERS = auto()
    REPEAT = auto()
    ROLL = auto()
    TRADE = auto()
    TUCK = auto()
    WHEN = auto()


class PowerMapper:
    _MAPPING = {
        PowerType.ALL: [
            ComponentType.PLAYERS, ComponentType.ACTION, ComponentType.N, ComponentType.ITEM,
            ComponentType.LOCATION, ComponentType.GROUP, ComponentType.ENTAILMENT, ComponentType.ACTION,
            ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION, ComponentType.END_GROUP,
            ComponentType.OPTIONAL, ComponentType.ASSERTION
        ],
        PowerType.DISCARD: [
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.OPTIONAL, ComponentType.ENTAILMENT, ComponentType.ACTION, ComponentType.N,
            ComponentType.ITEM, ComponentType.LOCATION, ComponentType.OPTIONAL, ComponentType.ASSERTION
        ],
        PowerType.DRAW: [
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.OPTIONAL, ComponentType.GROUP, ComponentType.ENTAILMENT, ComponentType.ACTION,
            ComponentType.N, ComponentType.GROUP, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.CONDITION, ComponentType.END_GROUP, ComponentType.OPTIONAL, ComponentType.END_GROUP,
            ComponentType.OPTIONAL, ComponentType.ASSERTION
        ],
        PowerType.EACH: [
            ComponentType.PLAYERS, ComponentType.ACTION, ComponentType.N, ComponentType.ITEM,
            ComponentType.LOCATION, ComponentType.CONDITION, ComponentType.ASSERTION
        ],
        PowerType.GAIN: [
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.GROUP, ComponentType.ENTAILMENT, ComponentType.ACTION, ComponentType.N,
            ComponentType.ITEM, ComponentType.LOCATION, ComponentType.END_GROUP, ComponentType.OPTIONAL,
            ComponentType.ASSERTION
        ],
        PowerType.IF: [
            ComponentType.IF, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.ACTION, ComponentType.ITEM, ComponentType.LOCATION, ComponentType.ASSERTION
        ],
        PowerType.LAY: [
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.ASSERTION
        ],
        PowerType.LOOK: [
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.IF_WS, ComponentType.ACTION, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.ELSE, ComponentType.ACTION, ComponentType.ITEM, ComponentType.ASSERTION
        ],
        PowerType.PLAY: [
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.CONDITION, ComponentType.ASSERTION
        ],
        PowerType.PLAYERS: [
            ComponentType.PLAYERS, ComponentType.CONDITION, ComponentType.ACTION, ComponentType.N,
            ComponentType.ITEM, ComponentType.LOCATION, ComponentType.OPTIONAL, ComponentType.ASSERTION
        ],
        PowerType.REPEAT: [
            ComponentType.ACTION, ComponentType.N, ComponentType.POWER, ComponentType.LOCATION,
            ComponentType.ASSERTION
        ],
        PowerType.ROLL: [
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.IF, ComponentType.N, ComponentType.CONDITION, ComponentType.ACTION,
            ComponentType.N, ComponentType.ITEM, ComponentType.ENTAILMENT, ComponentType.ACTION,
            ComponentType.ITEM, ComponentType.LOCATION, ComponentType.ASSERTION
        ],
        PowerType.TRADE: [
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.N,
            ComponentType.ITEM, ComponentType.LOCATION, ComponentType.ASSERTION
        ],
        PowerType.TUCK: [
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.ENTAILMENT, ComponentType.ACTION, ComponentType.N, ComponentType.ITEM,
            ComponentType.LOCATION, ComponentType.OPTIONAL, ComponentType.ASSERTION
        ],
        # TODO simplify somehow...
        PowerType.WHEN: [
            ComponentType.WHEN, ComponentType.PLAYERS, ComponentType.WHEN_COND,
            ComponentType.GROUP, ComponentType.GROUP, ComponentType.N, ComponentType.ITEM,
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.END_GROUP, ComponentType.OR, ComponentType.GROUP, ComponentType.ACTION,
            ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION, ComponentType.END_GROUP,
            ComponentType.OR, ComponentType.GROUP, ComponentType.CONDITION, ComponentType.ENTAILMENT,
            ComponentType.ACTION, ComponentType.N, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.ENTAILMENT, ComponentType.ACTION, ComponentType.ITEM, ComponentType.LOCATION,
            ComponentType.END_GROUP, ComponentType.END_GROUP, ComponentType.ASSERTION
        ],
    }

    @classmethod
    def get_components(cls, power_type: str) -> List[ComponentType]:
        return cls._MAPPING.get(power_type, None)
