import pygame, sys, asyncio
from pygame import mixer
import random

# Initialize Pygame
pygame.init()
# initialize mixer
mixer.init()
path_to_music_file = "assets/sounds/background.mp3"  # replace with the path to your mp3 file
mixer.music.load(path_to_music_file)  # load music
mixer.music.play(-1)  # play music, -1 means the music will loop indefinitely
# Screen dimensions
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (65, 105, 225)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vitya's life'")

# Fonts
font = pygame.font.Font(None, 36)


class Game:
    def __init__(self):
        self.level = [
            "####################",
            "#                  #",
            "#                  #",
            "#        ##        #",
            "#        ##        #",
            "#        ##        #",
            "#        ##        #",
            "#        ##        #",
            "#        ##        #",
            "#        ##        #",
            "#        ##        #",
            "#        ##        #",
            "#                  #",
            "#                  #",
            "####################"
        ]

        # Boxes names
        names = ["AUTH", "SCHED", "DOC", "FEE", "NOTI", "SD"]
        self.boxes = []
        self.targets = []
        self.player_direction = "down"
        self.generate_positions(names)
        self.player_pos = (1, 1)
        self.running = True

    def generate_positions(self, names):
        for name in names:
            while True:
                x = random.randint(2, len(self.level[0]) - 3)
                y = random.randint(2, len(self.level) - 3)

                # checking for walls
                if self.level[y][x] == "#":
                    continue

                if (x, y) in [box["coords"] for box in self.boxes] + self.targets:
                    continue
                self.boxes.append({'coords': (x, y), 'name': name})
                break
            while True:
                x = random.randint(2, len(self.level[0]) - 3)
                y = random.randint(2, len(self.level) - 3)

                # checking for walls
                if self.level[y][x] == "#":
                    continue

                if (x, y) in [box["coords"] for box in self.boxes] + self.targets:
                    continue
                self.targets.append((x, y))
                break

    def draw_level(self):
        for y, row in enumerate(self.level):
            for x, tile in enumerate(row):
                if tile == "#":
                    pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_boxes(self):
        for box in self.boxes:
            (x, y) = box['coords']
            name = box['name']

            box_img = pygame.image.load('assets/images/box.png')  # Load the box image
            box_img = pygame.transform.scale(box_img, (TILE_SIZE, TILE_SIZE))  # Scale the image
            screen.blit(box_img, (x * TILE_SIZE, y * TILE_SIZE))

            # Render the text
            font = pygame.font.Font(None, 15)
            text = font.render(name, True, BLACK, WHITE)

            # Calculate box center
            box_center = [x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2]

            # Calculate text center
            text_size = text.get_rect().size
            text_center = [text_size[0] / 2, text_size[1] / 2]

            # Calculate new position for the text
            text_pos = [box_center[0] - text_center[0], box_center[1] - text_center[1]]

            # Draw the text at the new position
            screen.blit(text, text_pos)

    def draw_player(self):
        x, y = self.player_pos

        # Load the player image based on direction
        player_img = pygame.image.load(f'assets/images/player/player_{self.player_direction}.png')

        # Scale the image
        player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

        # Draw the player at the new position
        screen.blit(player_img, (x * TILE_SIZE, y * TILE_SIZE))

    def draw_targets(self):
        for (x, y) in self.targets:
            pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)


    def move_player(self, dx, dy):
        px, py = self.player_pos
        new_pos = (px + dx, py + dy)

        if dx > 0:  # moving right
            self.player_direction = "right"
        elif dx < 0:  # moving left
            self.player_direction = "left"
        elif dy > 0:  # moving down
            self.player_direction = "down"
        elif dy < 0:  # moving up
            self.player_direction = "up"

        if self.is_wall(new_pos):
            return

        for box in self.boxes:
            if new_pos == box['coords']:
                new_box_pos = (new_pos[0] + dx, new_pos[1] + dy)
                if not self.is_wall(new_box_pos) and new_box_pos not in [b['coords'] for b in self.boxes]:
                    box['coords'] = new_box_pos
                    self.player_pos = new_pos
                    break
        else:
            self.player_pos = new_pos

    def is_wall(self, pos):
        x, y = pos
        return self.level[y][x] == "#"

    def check_win(self):
        return all(box['coords'] in self.targets for box in self.boxes)


async def main():
    game = Game()

    clock = pygame.time.Clock()

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_player(1, 0)
                elif event.key == pygame.K_UP:
                    game.move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    game.move_player(0, 1)

        screen.fill(WHITE)
        game.draw_level()
        game.draw_targets()
        game.draw_boxes()
        game.draw_player()

        if game.check_win():
            font = pygame.font.Font(None, 100)
            win_text = font.render("You are a loser!", True, BLACK, WHITE)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            game.running = False

        pygame.display.flip()
        clock.tick(60)

    await asyncio.sleep(0)

asyncio.run(main())