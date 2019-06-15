from tcod.console import Console


def render_all(console: Console, entities, game_map, colors):
    game_map.render(console=console, colors=colors)

    # Draw all entities in the list
    for entity in entities:
        if game_map.fov[entity.x, entity.y]:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)
