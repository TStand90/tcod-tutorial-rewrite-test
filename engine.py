# PART 1
# import tcod
# import tcod.event
#
# from input_handlers import handle_keys
#
#
# def main():
#     screen_width = 80
#     screen_height = 50
#
#     player_x = int(screen_width / 2)
#     player_y = int(screen_height / 2)
#
#     # Setup the font.
#     tcod.console_set_custom_font(
#         "arial10x10.png",
#         tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE,
#     )
#
#     # Initialize the root console in a context.
#     with tcod.console_init_root(
#         w=screen_width,
#         h=screen_height,
#         order="F",
#         renderer=tcod.RENDERER_SDL2,
#         vsync=True
#     ) as root_console:
#         while True:
#             # Display a basic test message
#             # root_console.print(x=0, y=0, string='Hello World!', fg=tcod.white)
#             root_console.print(x=player_x, y=player_y, string='@', fg=tcod.white)
#
#             # Show the console
#             tcod.console_flush()
#
#             # Clear the console, so that when the characters move, they aren't redrawn in their original positions.
#             root_console.clear()
#
#             for event in tcod.event.wait():
#                 if event.type == 'QUIT':
#                     raise SystemExit()
#
#                 if event.type == 'KEYDOWN':
#                     action = handle_keys(event.sym, event.mod)
#
#                     move = action.get('move')
#                     full_screen = action.get('fullscreen')
#                     escape = action.get('escape')
#
#                     if move:
#                         dx, dy = move
#                         player_x += dx
#                         player_y += dy
#
#                     if full_screen:
#                         tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
#
#                     if escape:
#                         raise SystemExit()
#
#
# if __name__ == '__main__':
#     main()


import tcod
import tcod.event

from entity import Entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import render_all


def main():
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150)
    }

    game_map = GameMap(map_width, map_height)

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.white)
    npc = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.yellow)
    entities = [npc, player]

    # Setup the font.
    tcod.console_set_custom_font(
        "arial10x10.png",
        tcod.FONT_LAYOUT_TCOD | tcod.FONT_TYPE_GREYSCALE,
    )

    # Initialize the root console in a context.
    with tcod.console_init_root(
        w=screen_width,
        h=screen_height,
        order="F",
        renderer=tcod.RENDERER_SDL2,
        vsync=True
    ) as root_console:
        while True:
            render_all(root_console, entities, game_map, colors)

            # Show the console
            tcod.console_flush()

            # Clear the console, so that when the characters move, they aren't redrawn in their original positions.
            root_console.clear()

            for event in tcod.event.wait():
                if event.type == 'QUIT':
                    raise SystemExit()

                if event.type == 'KEYDOWN':
                    action = handle_keys(event.sym, event.mod)

                    move = action.get('move')
                    full_screen = action.get('fullscreen')
                    escape = action.get('escape')

                    if move:
                        dx, dy = move

                        if not game_map.is_blocked(player.x + dx, player.y + dy):
                            player.move(dx, dy)

                    if full_screen:
                        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

                    if escape:
                        raise SystemExit()


if __name__ == '__main__':
    main()
