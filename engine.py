import tcod
import tcod.event

from entity import Entity, get_blocking_entities_at_location
from game_states import GameStates
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import render_all


def main():
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 12
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True)
    entities = [player]

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                      max_monsters_per_room)

    fov_recompute = True

    game_state = GameStates.PLAYERS_TURN

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
            if fov_recompute:
                game_map.compute_fov(player.x, player.y, radius=fov_radius, light_walls=fov_light_walls,
                                     algorithm=fov_algorithm)

            render_all(root_console, entities, game_map, colors)

            fov_recompute = False

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

                    if move and game_state == GameStates.PLAYERS_TURN:
                        dx, dy = move
                        destination_x = player.x + dx
                        destination_y = player.y + dy

                        if not game_map.is_blocked(player.x + dx, player.y + dy):
                            if not game_map.is_blocked(destination_x, destination_y):
                                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                                if target:
                                    print(f'You kick the {target.name} in the shins, much to its annoyance!')
                                else:
                                    player.move(dx, dy)

                                    fov_recompute = True

                                game_state = GameStates.ENEMY_TURN

                    if full_screen:
                        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

                    if game_state == GameStates.ENEMY_TURN:
                        for entity in entities:
                            if entity != player:
                                print(f'The {entity.name} ponders the meaning of its existence.')

                        game_state = GameStates.PLAYERS_TURN

                    if escape:
                        raise SystemExit()


if __name__ == '__main__':
    main()
