# PART 1
# import tcod.event
#
#
# def handle_keys(key, modifier=None):
#     if key == tcod.event.K_UP:
#         return {'move': (0, -1)}
#     elif key == tcod.event.K_DOWN:
#         return {'move': (0, 1)}
#     elif key == tcod.event.K_LEFT:
#         return {'move': (-1, 0)}
#     elif key == tcod.event.K_RIGHT:
#         return {'move': (1, 0)}
#
#     if key == tcod.event.K_RETURN and modifier & tcod.event.KMOD_LALT:
#         # Alt+Enter: toggle full screen
#         return {'fullscreen': True}
#
#     elif key == tcod.event.K_ESCAPE:
#         # Exit the game
#         return {'escape': True}
#
#     # No key was pressed
#     return {}

import tcod.event


def handle_keys(key, modifier=None):
    if key == tcod.event.K_UP:
        return {'move': (0, -1)}
    elif key == tcod.event.K_DOWN:
        return {'move': (0, 1)}
    elif key == tcod.event.K_LEFT:
        return {'move': (-1, 0)}
    elif key == tcod.event.K_RIGHT:
        return {'move': (1, 0)}

    if key == tcod.event.K_RETURN and modifier & tcod.event.KMOD_LALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key == tcod.event.K_ESCAPE:
        # Exit the game
        return {'escape': True}

    # No key was pressed
    return {}
