from enum import auto, Enum

from tcod.console import Console


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def render_all(console: Console, entities, player, game_map, screen_width, screen_height, colors):
    game_map.render(console=console, colors=colors)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        if game_map.fov[entity.x, entity.y]:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

    # tcod.console_set_default_foreground(con, libtcod.white)
    # tcod.console_print_ex(con, 1, screen_height - 2, libtcod.BKGND_NONE, libtcod.LEFT,
    #                          'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))

    console.print(x=1, y=screen_height - 2, string=f'HP: {player.fighter.hp}/{player.fighter.max_hp}')
