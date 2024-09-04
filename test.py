import pygame
pygame.init()
import random
import pygame_menu
import os

background_image = pygame.image.load('background.png')  
background_image = pygame.transform.scale(background_image, (500, 600))

font = pygame.font.Font(None, 36)
high_score = 0
score = 0
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0
# створення головного вікна
window_size = (500, 600)
window = pygame.display.set_mode(window_size)

class Player:
    def __init__(self, x, y, width, height, image):
        self.original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original_image, (width, height))  # Зміна розміру зображення
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.gravity = 0.5
        self.jump_power = -10
        self.vel_y = 0
        self.can_jump = False
        self.jumps = 2


    def move(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for w in walls:
            if self.rect.colliderect(w.rect):              
                self.jumps = 2
            
                if self.vel_y > 0:
                    self.rect.bottom = w.rect.top
                    self.vel_y = 0
                    self.can_jump = True

    def jump(self):
        if self.can_jump:
            self.vel_y = self.jump_power
            if self.jumps <= 1:     
                self.can_jump = False
            self.jumps -= 1 

    def move_horizontal(self, dx):
        self.jumps = 2
        self.rect.x += dx


class Wall:
    def __init__(self, x, y, width, height, color=(22, 26, 31)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.passed = False  # Додаємо прапорець для відстеження, чи платформа вже пройдена

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

if score >= 0 and score < 10:
    image2 = "player.png"
    image1 = 'player-reverse.png'
elif score > 10 and score < 20:
    image2 = "player_white.png"
    image1 = 'player_white_reverse.png'
    background_image = "background_lvl10.png"
elif score >= 20 and score < 30:
    image2 = "player_blue.png"
    image1 = 'player_blue_reverse.png'
    background_image = "background_lvl20.jpg"
elif score > 30 and score < 40:
    image2 = "player_yellow.png"
    image1 = 'player_yellow-reverse.png'
    background_image = "background_lvl30.jpg"
elif score >= 40 and score < 50:
    image2 = "player_beast.png"
    image1 = 'player_beast_reverse.png'
    background_image = "background_lvl40.png"


imagecoin = "money.png"


# створення персонажа
player = Player(100, 100, 50, 50, image1)
coin = Player(100, 100, 50, 50, image1)

# створення стін
walls = [
    Wall(20, 500, 200, 20),
    Wall(350, 400, 150, 20),
    Wall(100, 300, 200, 20),
]

# Параметри спавну платформ
wall_width = 100
wall_height = 20
min_gap = 100  # Мінімальна відстань між платформами по вертикалі
max_gap = 200  # Максимальна відстань між платформами по вертикалі



def start_game():
    global high_score, walls, score, background_image
    # кольори
    white = (255, 255, 255)

    # створення об'єкту "годинник" для встановлення частоти кадрів
    clock = pygame.time.Clock()

    # головний цикл гри
    game = True
    move_left = False
    move_right = False

    pygame.mixer.music.load('background_music.wav')
    pygame.mixer.music.play(-1)


    # Список для відстеження, чи платформи пройдені
    passed_walls = set()

    while game:
        if score >= 0 and score < 10:
            image2 = "player.png"
            image1 = 'player-reverse.png'
        elif score > 10 and score < 20:
            image2 = "player_white (1).png"
            image1 = 'player_white_reverse (1).png'
            background_image = "background_lvl10.png"
        elif score >= 20 and score < 30:
            image2 = "player_blue(1).png"
            image1 = 'player_blue_reverse (1).png'
            background_image = "background_lvl20.jpg"
        elif score > 30 and score < 40:
            image2 = "player_yellow (1).png"
            image1 = 'player_yellow-reverse (1).png'
            background_image = "background_lvl30.jpg"
        elif score >= 40 and score < 50:
            image2 = "player_beast (1).png"
            image1 = 'player_beast_reverse (1).png'
            background_image = "background_lvl40.png"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    move_right = True
                    player.original_image = pygame.image.load(image1)
                    player.image = pygame.transform.scale(player.original_image, (50, 50))
                if event.key == pygame.K_a:
                    move_left = True
                    player.original_image = pygame.image.load(image2)
                    player.image = pygame.transform.scale(player.original_image, (50, 50))
                if event.key == pygame.K_w:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_a:
                    move_left = False

        window.blit(background_image, (0, 0))
        player.move()

        if move_right:
            player.move_horizontal(3)
        if move_left:
            player.move_horizontal(-3)

        # Оновлення стану платформ
        for wall in walls:
            wall.draw(window)
            wall.rect.y += 1

        # Перевірка, чи персонаж пройшов платформу
        for wall in walls:
            if wall not in passed_walls:
                # Перевірка, чи персонаж проходить через платформу
                if (player.rect.top < wall.rect.bottom and player.rect.bottom > wall.rect.top and
                    player.rect.centerx > wall.rect.left and player.rect.centerx < wall.rect.right):
                    passed_walls.add(wall)
                    score += 1

        if score > high_score:
            high_score = score

        text = font.render(f"Рахунок: {score}", True, (255,0,0))
        text2 = font.render(f"Мій Рахунок: {high_score}", True, (255,0,0))

        window.blit(player.image, (player.rect.x, player.rect.y))
        window.blit(coin.image, (coin.rect.x, coin.rect.y))

        # Спавн нових платформ
        if len(walls) < 10:  # Підтримка певної кількості платформ на екрані
            if len(walls) == 0:
                # Перша платформа
                start_x = random.randint(0, window_size[0] - wall_width)
                start_y = window_size[1] - 100
                walls.append(Wall(start_x, start_y, wall_width, wall_height))
            else:
                # Спавн нових платформ
                last_wall = walls[-1]
                last_x = last_wall.rect.x
                last_y = last_wall.rect.top

                new_x = random.randint(0, window_size[0] - wall_width)
                new_y = last_y - random.randint(min_gap, max_gap)

                # Переконатися, що нова платформа не перекриває існуючі
                while any(w.rect.colliderect(pygame.Rect(new_x, new_y, wall_width, wall_height)) for w in walls):
                    new_x = random.randint(0, window_size[0] - wall_width)
                    new_y = last_y - random.randint(min_gap, max_gap)

                walls.append(Wall(new_x, new_y, wall_width, wall_height))


                
        # Видалення платформ, що вийшли за межі екрану
        walls = [w for w in walls if w.rect.y < window_size[1]]

        with open("score.txt", "w") as file:
            file.write(str(high_score))
            
        window.blit(text2,(10,50))
        window.blit(text,(10,10))

        clock.tick(60)
        pygame.display.update()

    pygame.quit()
    pygame.mixer.music.stop()


def skins_menu():
    menu = pygame_menu.Menu('Skin Menu', *window_size, theme=pygame_menu.themes.THEME_GREEN)

    menu.add.button('Return', pygame_menu.events.BACK)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        menu.update(events)
        menu.draw(window)
        pygame.display.update()
        
# def set_skin(value, skin):
#     global selected_skin
#     selected_skin = skin

# def skin_menu():
#     menu = pygame_menu.Menu('Choose Your Skin', *window_size, theme=pygame_menu.themes.THEME_DARK)
#     menu.add.selector('Select Skin: ', [('Default', 'player.png'), ('Reverse', 'player-reverse.png')], onchange=set_skin)
#     menu.add.button('Back', main_menu)
#     menu.mainloop(window)

def main_menu():
    menu = pygame_menu.Menu('Main Menu', *window_size, theme=pygame_menu.themes.THEME_GREEN)
    menu.add.button('Start Game', start_game)
    #menu.add.button('Choose Skin', skin_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        menu.update(events)
        menu.draw(window)
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
