from random import randint

from tcod.map import Map

from map_objects.rectangle import Rect


class GameMap(Map):
    def __init__(self, width, height):
        super().__init__(width, height, order='F')

        self.initialize_tiles()

    def create_h_tunnel(self, x1, x2, y):
        min_x = min(x1, x2)
        max_x = max(x1, x2) + 1

        self.walkable[min_x:max_x, y] = True
        self.transparent[min_x:max_x, y] = True

    def create_room(self, room: Rect):
        self.walkable[room.x1 + 1:room.x2, room.y1 + 1:room.y2] = True
        self.transparent[room.x1 + 1:room.x2, room.y1 + 1:room.y2] = True

    def create_v_tunnel(self, y1, y2, x):
        min_y = min(y1, y2)
        max_y = max(y1, y2) + 1

        self.walkable[x, min_y:max_y] = True
        self.transparent[x, min_y:max_y] = True

    def initialize_tiles(self):
        self.transparent[:] = False
        self.walkable[:] = False

    def is_blocked(self, x, y):
        return not self.walkable[x, y]

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            width = randint(room_min_size, room_max_size)
            height = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - width - 1)
            y = randint(0, map_height - height - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, width, height)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

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
