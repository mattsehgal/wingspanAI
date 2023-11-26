from src.parsing.enums.base import AutoName
from enum import auto

from typing import List


class ComponentType(AutoName):
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

    @classmethod
    def _compound(cls, name: str) -> List["ComponentType"]:
        if name == '*ANIL':
            return [cls.ACTION, cls.N, cls.ITEM, cls.LOCATION]
        else:
            return []

    @classmethod
    def list_from_names(cls, names: List[str]) -> List["ComponentType"]:
        ctypes = []
        for name in names:
            if '*' in name:
                ctypes.extend(cls._compound(name))
            else:
                ctypes.append(cls.__members__[name])
        return ctypes


class ComponentRegex(AutoName):
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


class PowerType(AutoName):
    ALL = auto()
    DISCARD = auto()
    DRAW = auto()
    EACH = auto()
    GAIN = auto()
    IF = auto()
    LAY = auto()
    LOOK = auto()
    NONE = auto()
    PLAY = auto()
    PLAYERS = auto()
    REPEAT = auto()
    ROLL = auto()
    TRADE = auto()
    TUCK = auto()
    WHEN = auto()


class PowerMapper:
    _MAPPING = {
        PowerType.ALL: ComponentType.list_from_names(
            [
                'PLAYERS', '*ANIL',
                'GROUP', 'ENTAILMENT', '*ANIL', 'END_GROUP',
                'OPTIONAL', 'ASSERTION'
            ]
        ),
        PowerType.DISCARD: ComponentType.list_from_names(
            [
                '*ANIL', 'OPTIONAL', 'ENTAILMENT',
                '*ANIL', 'OPTIONAL', 'ASSERTION'
            ]
        ),
        PowerType.DRAW: ComponentType.list_from_names(
            [
                '*ANIL', 'OPTIONAL',
                'GROUP', 'ENTAILMENT', 'ACTION', 'N',
                'GROUP', 'ITEM', 'LOCATION', 'CONDITION',
                'END_GROUP', 'OPTIONAL',
                'END_GROUP', 'OPTIONAL', 'ASSERTION'
            ]
        ),
        PowerType.EACH: ComponentType.list_from_names(
            [
                'PLAYERS', '*ANIL', 'CONDITION', 'ASSERTION'
            ]
        ),
        PowerType.GAIN: ComponentType.list_from_names(
            [
                '*ANIL',
                'GROUP', 'ENTAILMENT', '*ANIL', 'END_GROUP',
                'OPTIONAL', 'ASSERTION'
            ]
        ),
        PowerType.IF: ComponentType.list_from_names(
            [
                'IF', 'N', 'ITEM', 'LOCATION',
                'ACTION', 'ITEM', 'LOCATION', 'ASSERTION'
            ]
        ),
        PowerType.LAY: ComponentType.list_from_names(
            [
                '*ANIL', 'ASSERTION'
            ]
        ),
        PowerType.LOOK: ComponentType.list_from_names(
            [
                '*ANIL',
                'IF_WS', 'ACTION', 'ITEM', 'LOCATION',
                'ELSE', 'ACTION', 'ITEM', 'ASSERTION'
            ]
        ),
        PowerType.NONE: [],
        PowerType.PLAY: ComponentType.list_from_names(
            [
                '*ANIL', 'CONDITION', 'ASSERTION'
            ]
        ),
        PowerType.PLAYERS: ComponentType.list_from_names(
            [
                'PLAYERS', 'CONDITION', '*ANIL', 'OPTIONAL', 'ASSERTION'
            ]
        ),
        PowerType.REPEAT: ComponentType.list_from_names(
            [
                'ACTION', 'N', 'POWER', 'LOCATION', 'ASSERTION'
            ]
        ),
        PowerType.ROLL: ComponentType.list_from_names(
            [
                '*ANIL',
                'IF', 'N', 'CONDITION', 'ACTION', 'N', 'ITEM',
                'ENTAILMENT', 'ACTION', 'ITEM', 'LOCATION', 'ASSERTION'
            ]
        ),
        PowerType.TRADE: ComponentType.list_from_names(
            [
                'ACTION', 'N', 'ITEM', 'N', 'ITEM', 'LOCATION', 'ASSERTION'
            ]
        ),
        PowerType.TUCK: ComponentType.list_from_names(
            [
                '*ANIL', 'ENTAILMENT', '*ANIL', 'OPTIONAL', 'ASSERTION'
            ]
        ),

        # TODO simplify?
        PowerType.WHEN: ComponentType.list_from_names(
            [
                'WHEN', 'PLAYERS', 'WHEN_COND',
                'GROUP',
                'GROUP', 'N', 'ITEM', '*ANIL',
                'END_GROUP', 'OR',
                'GROUP', '*ANIL',
                'END_GROUP', 'OR',
                'GROUP', 'CONDITION', 'ENTAILMENT', '*ANIL',
                'ENTAILMENT', 'ACTION', 'ITEM', 'LOCATION',
                'END_GROUP', 'END_GROUP', 'ASSERTION'
            ]
        ),
    }

    @classmethod
    def get_components(cls, power_type: str) -> List[ComponentType]:
        return cls._MAPPING.get(power_type, None)
