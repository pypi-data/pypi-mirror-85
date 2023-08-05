from enum import IntEnum


class EyeMovementTypes(IntEnum):
    """An enumeration for the different types of eye movements.

    In case you want to implement your own eye movement class that is not yet present (glissades, regressions,...)
    please use the CUSTOM type and add a (unique) number to it (e.g., EyeMovementTypes.CUSTOM+2823), to avoid collisions
    as far as possible - or define your own and do a push request :-)
    """
    FIXATION = 1
    SACCADE = 2
    SMOOTH_PURSUIT = 3
    MICRO_SACCADE = 4
    VESTIBULO_OCULAR_REFLEX = 5
    BLINK = 6
    GAP = 7
    CUSTOM = 100
