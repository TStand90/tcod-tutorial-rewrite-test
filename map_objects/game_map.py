from tcod.map import Map


class GameMap(Map):
    def __init__(self, width, height):
        super().__init__(width, height, order='F')

        self.initialize_tiles()

    def initialize_tiles(self):
        self.transparent[:] = True
        self.walkable[:] = True

        self.walkable[30:32, 22] = False

    def is_blocked(self, x, y):
        return not self.walkable[x, y]

    def render(self, console, colors):
        """
        Draw all the tiles in the game map. Assume that a tile that is not "blocked" is a wall.
        """
        for y in range(self.height):
            for x in range(self.width):
                wall = self.is_blocked(x, y)

                if wall:
                    console.print(x=x, y=y, string=' ', bg=colors.get('dark_wall'))
                else:
                    console.print(x=x, y=y, string=' ', bg=colors.get('dark_ground'))
