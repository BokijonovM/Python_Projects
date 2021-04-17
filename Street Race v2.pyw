import pygame as pg
import pygame.freetype
import random
import os
import math

os.environ['SDL_VIDEO_CENTERED'] = '1'
path = os.path.dirname(os.path.abspath(__file__))
record_file = os.path.join(path, 'Record', 'record.txt')
try:
    with open(record_file, 'x') as f:
        f.write(str(0))
except (BaseException, OSError):
    pass

SIZE = WIDTH, HEIGHT = 800, 600
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
WHITE = (200, 200, 200)
RED = (230, 0, 0)
rgb = [0, 250, 0]
block = False
pause = [False, True]
count = [0]
car_accident = 0
level = 40
start = 255
blink = 0
hit_old = None


def icon():
    size, text = 32, '\u0056\u004F'
    sur = pg.Surface((size, size), pg.SRCALPHA)
    pg.draw.circle(
        sur, '#44475a59', (size // 2, size // 2), size // 2)
    font_text = pg.freetype.SysFont('Arial', 16, True)
    rect = font_text.get_rect(text)
    x, y = (size - rect.width) // 2, (size - rect.height) // 2
    font_text.render_to(sur, (x, y), text, fgcolor='#ff0000')
    pg.display.set_icon(sur)


pg.init()
icon()
pg.display.set_caption('Rally')
screen = pg.display.set_mode(SIZE)

FPS = 120
clock = pg.time.Clock()
font = pygame.freetype.Font(os.path.join(path, 'font', 'seguisym.ttf'), 30)

cars = [pg.image.load(os.path.join(path, 'img', 'car1.png')),
        pg.image.load(os.path.join(path, 'img', 'car2.png')),
        pg.image.load(os.path.join(path, 'img', 'car3.png'))]
alarm = [pg.image.load(os.path.join(path, 'alarm', '1.png')),
         pg.image.load(os.path.join(path, 'alarm', '2.png'))]
sound_car_accident = pg.mixer.Sound(os.path.join(path, 'sound', 'udar.wav'))
sound_canister = pg.mixer.Sound(os.path.join(path, 'sound', 'canister.wav'))
sound_accident = pg.mixer.Sound(os.path.join(path, 'sound', 'accident.wav'))

button_start = pg.image.load(os.path.join(path, 'img', 'btn_play.png'))
button_start_rect = button_start.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
button_stop = pg.image.load(os.path.join(path, 'img', 'btn_exit.png'))
button_stop_rect = button_stop.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

fuel_image = pg.image.load(os.path.join(path, 'img', 'fuel.png'))
canister_image = pg.image.load(os.path.join(path, 'img', 'canister.png'))
water_image = pg.image.load(os.path.join(path, 'img', 'water.png'))

u1_event = pg.USEREVENT + 1
pg.time.set_timer(u1_event, random.randrange(6000, 26001, 4000))
u2_event = pg.USEREVENT + 2
pg.time.set_timer(u2_event, random.randrange(13000, 28001, 5000))


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(path, 'img', 'car4.png'))
        self.orig_image = self.image
        self.angle = 0
        self.speed = 2
        self.acceleration = 0.02
        self.rect = self.image.get_rect(center=(WIDTH - 20, HEIGHT - 70))
        self.position = pg.math.Vector2()
        self.velocity = pg.math.Vector2()
        self.vx = 0  # velocity.x for speedometer

    def update(self):
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.position += self.velocity
        self.rect = self.image.get_rect(center=self.position)

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
            self.angle -= 1
            self.vx -= self.acceleration
            if self.angle < -25:
                self.angle = -25
        elif keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
            self.angle += 1
            self.vx -= self.acceleration
            if self.angle > 25:
                self.angle = 25
        else:
            self.vx += self.acceleration if self.vx < 0 else 0
            self.velocity.x = 0
            if self.angle < 0:
                self.angle += 1
            elif self.angle > 0:
                self.angle -= 1
        if keys[pg.K_UP]:
            self.velocity.y -= self.acceleration
            if self.velocity.y < -self.speed:
                self.velocity.y = -self.speed
        elif keys[pg.K_DOWN]:
            self.velocity.y += self.acceleration
            if self.velocity.y > self.speed:
                self.velocity.y = self.speed
        else:
            if self.velocity.y < 0:
                self.velocity.y += self.acceleration
                if self.velocity.y > 0:
                    self.velocity.y = 0
            elif self.velocity.y > 0:
                self.velocity.y -= self.acceleration
                if self.velocity.y < 0:
                    self.velocity.y = 0

    def for_speedometer(self):
        if self.vx <= -0.4:
            self.vx = -0.4  # left-right speedometer max
        if self.velocity.y < self.vx or self.velocity.y > 0:
            self.vx = self.velocity.y
            if self.vx >= 1.04:
                self.vx = 1.04  # speedometer min for speed=2
        return self.vx


class Alarm(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.images = alarm
        self.index = 0
        self.range = len(self.images)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.speed = 1

    def update(self):
        self.index += 0.02
        self.image = self.images[int(self.index % self.range)]
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, img):
        pg.sprite.Sprite.__init__(self)

        if img == fuel_image:
            self.image = img
            self.speed = 0
        elif img == canister_image or img == water_image:
            self.image = img
            self.speed = 1
        else:
            self.image = pg.transform.flip(img, False, True)
            self.speed = random.randint(2, 3)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            if self is canister or self is water:
                self.kill()
            else:
                if 40 < player.rect.centerx < WIDTH - 40 \
                        and player.rect.top < HEIGHT and player.rect.bottom > 0:
                    count[0] += 1
                list_x.remove(self.rect.centerx)
                while True:
                    self.rect.centerx = random.randrange(80, WIDTH, 80)
                    if self.rect.centerx in list_x:
                        continue
                    else:
                        list_x.append(self.rect.centerx)
                        self.speed = random.randint(2, 3)
                        self.rect.bottom = 0
                        break


class Road(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface(screen.get_size())
        self.image.fill(GREY)
        pg.draw.line(self.image, GREEN, (20, 0), (20, 600), 40)
        pg.draw.line(self.image, GREEN, (780, 0), (780, 600), 40)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(
                    self.image, WHITE,
                    (40 + xx * 80, 0 if xx == 0 or xx == 9 else 10 + yy * 60),
                    (40 + xx * 80, 600 if xx == 0 or xx == 9 else 50 + yy * 60), 5)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0


class Volume(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 140), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = 10
        self.x = self.y = self.radius
        self.color_circle = (0, 255, 0, 128)
        self.color_rect = (0, 180, 0, 128)
        self.color_text = (255, 255, 255)
        self.alpha = 255
        self.volume = 1

    def update(self):
        self.image.set_alpha(self.alpha)
        pg.draw.rect(
            self.image, self.color_rect, [0, 0, *self.rect[2:]],
            border_radius=self.radius)
        pg.draw.circle(self.image, self.color_circle, (self.x, self.y), self.radius)
        text = str(round(self.volume * 100))
        text_rect = font.get_rect(text, size=11)
        font.render_to(
            self.image, (self.x - text_rect[2] / 2., self.y - text_rect[3] / 2.), text,
            self.color_text, rotation=0, size=11)
        sp = "\U0001F507" if self.volume == 0 else "\U0001F508" if self.volume < 0.2 \
            else "\U0001F509" if self.volume < 0.7 else "\U0001F50A"
        font.render_to(
            screen, (self.rect.x, self.rect.y - font.size), sp, [*WHITE, self.alpha])

    def render(self, e_buttons, e_pos):
        if self.rect.left < e_pos[0] < self.rect.right and \
                self.rect.top < e_pos[1] < self.rect.bottom and \
                e_buttons:
            self.y = abs(self.rect.top - e_pos[1])
            if self.y > self.rect.h - self.radius:
                self.y = self.rect.h - self.radius
            elif self.y < self.radius:
                self.y = self.radius
            self.volume = (100 - (self.y - self.radius) / 1.2) / 100.
            sound_car_accident.set_volume(self.volume)
            sound_canister.set_volume(self.volume)
            sound_accident.set_volume(self.volume)


class Speedometer(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        w, h = 150, 150
        self.radius = 140
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        self.rect = self.image.get_rect(bottomright=(WIDTH, HEIGHT))
        font.render_to(self.image, (w - 50, h - 50), 'km/h', WHITE, size=20)
        for deg in range(5, 84, 6):
            length = 18 if deg == 5 or deg == 23 or deg == 41 or deg == 59 or deg == 77 else 10
            cos = math.cos(math.radians(deg))
            sin = math.sin(math.radians(deg))
            pg.draw.line(
                self.image, WHITE,
                (w - self.radius * cos, h - self.radius * sin),
                (w - (self.radius - length) * cos, h - (self.radius - length) * sin), 2)
        for value, deg in enumerate(range(9, 78, 17)):
            cos = math.cos(math.radians(deg))
            sin = math.sin(math.radians(deg))
            font.render_to(self.image, (
                round(w - (self.radius - 30) * cos), round(h - (self.radius - 30) * sin)),
                str(value * 100), WHITE, size=15)

    def render(self):
        s = 30 - player.for_speedometer() * 25  # from 4 to 80
        pg.draw.line(
            screen, RED, self.rect.bottomright,
            (self.rect.right - (self.radius - 10) * math.cos(math.radians(s)),
             self.rect.bottom - (self.radius - 10) * math.sin(math.radians(s))), 4)
        pg.draw.circle(screen, WHITE, self.rect.bottomright, 25)
        vol.update()


all_sprite = pg.sprite.LayeredUpdates()
cars_group = pg.sprite.Group()
canister_group = pg.sprite.Group()
for r in range(2):
    all_sprite.add(Road(0, 0 if r == 0 else -HEIGHT), layer=0)
speedometer = Speedometer()
all_sprite.add(speedometer, layer=0)
player = Player()

list_x = []
n = 0
while n < 6:
    car_x = random.randrange(80, WIDTH, 80)
    if car_x in list_x:
        continue
    else:
        list_x.append(car_x)
        cars_group.add(Car(car_x, random.randint(
            -cars[0].get_height() * 3, -cars[0].get_height()),
            cars[n] if n < 3 else random.choice(cars)))
        n += 1

fuel = Car(WIDTH - 80, 40, fuel_image)
canister = Car(0, 0, canister_image)
water = Car(0, 0, water_image)
vol = Volume(20, HEIGHT - 80)

all_sprite.add(*cars_group, layer=1)
all_sprite.add(player, layer=3)
all_sprite.add(fuel, layer=4)
all_sprite.add(vol, layer=4)


def my_record():
    with open(record_file, 'r+') as d:
        record = d.read()
        if count[0] > int(record):
            record = str(count[0])
            d.seek(0)
            d.truncate()
            d.write(record)
    return record


def home_screen(b):
    screen.blit(all_sprite.get_sprite(0).image, (0, 0))
    screen.blit(speedometer.image, speedometer.rect)
    button_start.set_alpha(start)
    button_stop.set_alpha(start)
    screen.blit(button_start, button_start_rect)
    screen.blit(button_stop, button_stop_rect)
    font.render_to(screen, (48, 10), f'Record: {rec}', [
        *RED, 255 if count[0] <= record_old else 255 if int(b) % 2 else 0], size=24)
    font.render_to(screen, (48, 40), f'Points: {count[0]}', RED, size=24)
    font.render_to(screen, (48, 70), f'Accidents: {car_accident}', RED, size=24)
    vol.update()
    screen.blit(vol.image, vol.rect)


rec = my_record()
record_old = int(rec)
game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            game = False
        elif e.type == pg.KEYDOWN and e.key == pg.K_p and start == 0:
            pause.reverse()
            if pause[0]:
                pg.mouse.set_visible(True)
                vol.alpha = 255
            else:
                pg.mouse.set_visible(False)
                vol.alpha = 0
        elif e.type == pg.MOUSEMOTION and (start == 255 or pause[0]):
            vol.render(e.buttons[0], e.pos)
        elif e.type == pg.MOUSEBUTTONDOWN and start == 255:
            if e.button == 1:
                if button_start_rect.collidepoint(e.pos):
                    player.angle = 0
                    player.velocity.x, player.velocity.y = 0, 0
                    player.position.x, player.position.y = WIDTH - 20, HEIGHT - 70
                    player.update()
                    all_sprite.remove_sprites_of_layer(2)
                    water.kill()
                    canister.kill()
                    for cr in cars_group:
                        cr.speed = random.randint(2, 3)
                        cr.rect.bottom = 0
                    level = 40
                    car_accident = 0
                    count[0] = 0
                    start -= 1
                    record_old = int(rec)
                    pg.mouse.set_visible(False)
                elif button_stop_rect.collidepoint(e.pos):
                    game = False
        elif e.type == u1_event and not pause[0] and not all_sprite.has(water):  # water.alive():
            all_sprite.add(water, layer=0)
            water.rect.center = \
                random.randrange(80, WIDTH, 80), -water.rect.h
            timer1 = random.randrange(6000, 26001, 4000)
            pg.time.set_timer(u1_event, timer1)
        elif e.type == u2_event and not pause[0] and not canister_group.has(canister):
            canister_group.add(canister)
            all_sprite.add(canister, layer=0)
            canister.rect.center = \
                random.randrange(80, WIDTH, 80), -canister.rect.h
            timer2 = random.randrange(13000, 28001, 5000)
            pg.time.set_timer(u2_event, timer2)

    hit = pg.sprite.spritecollideany(player, cars_group)  # hit -> sprite car
    if hit and hit.speed != 1:
        player.position.x += 50 * random.randrange(-1, 2, 2)
        player.angle = 50 * random.randrange(-1, 2, 2)
        hit.speed = 1
        car_alarm = Alarm()
        all_sprite.add(car_alarm, layer=2)
        car_alarm.rect.center = hit.rect.center
        car_accident += 1
        if car_accident > 10:
            car_accident = 10
        sound_car_accident.play()
    if pg.sprite.spritecollide(player, canister_group, True):
        level = 40
        sound_canister.play()
    if pg.sprite.collide_rect(player, water):
        if not block:
            player.angle = random.randint(60, 90) * random.randrange(-1, 2, 2)
            sound_accident.play()
            block = True
    else:
        block = False

    if start > 0:
        home_screen(blink)
        blink = 0 if blink > 99 else blink + .02
        if start != 255:
            start -= 1
            vol.alpha = start
    else:
        if not pause[0]:
            level -= .01
            if level < 0 or car_accident > 9:
                start = 255
                rec = my_record()
                pg.mouse.set_visible(True)
                vol.alpha = start
            elif level < 10:
                rgb[:2] = 250, 0
            elif level < 20:
                rgb[0] = 250
            else:
                rgb[:2] = 0, 250

            all_sprite.update()
        else:
            vol.update()

        all_sprite.draw(screen)
        pg.draw.rect(
            screen, rgb,
            (fuel.rect.left + 10, fuel.rect.bottom - level - 8, 21, level))
        font.render_to(screen, (48, 10), f'accidents: {car_accident}', GREEN, size=24)
        font.render_to(screen, (48, HEIGHT - 30), f'{count[0]}', GREEN, size=24)

    speedometer.render()  # speedometer
    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Rally      FPS: {int(clock.get_fps())}')

# pg.image.save(screen, 'road.jpg')
