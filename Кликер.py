import pygame
import random
import math
FPS = 60
# sound1 = pygame.mixer.Sound('boom.wav')
# animCount = 0
# delay = 100

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
   rect = pygame.Rect(rect)
   y = rect.top
   lineSpacing = -2

   # get the height of the font
   fontHeight = font.size("Tg")[1]

   while text:
       i = 1

       # determine if the row of text will be outside our area
       if y + fontHeight > rect.bottom:
           break

       # determine maximum width of line
       while font.size(text[:i])[0] < rect.width and i < len(text):
           i += 1

       # if we've wrapped the text, then adjust the wrap to the last word
       if i < len(text):
           i = text.rfind(" ", 0, i) + 1

       # render the line and blit it to the surface
       if bkg:
           image = font.render(text[:i], 1, color, bkg)
           image.set_colorkey(bkg)
       else:
           image = font.render(text[:i], aa, color)

       surface.blit(image, (rect.left, y))
       y += fontHeight + lineSpacing

       # remove the text we just blitted
       text = text[i:]

   return text

sc = pygame.display.set_mode((1920, 1080))


def draw_stroke(name, font, surface=sc, pos=(0, 0), text_color=(255, 255, 255), stroke_color=(0, 0, 0), pixel=2):
    text = font.render(name, True, text_color)
    stroke = font.render(name, True, stroke_color)
    surface.blit(stroke, (pos[0] - pixel, pos[1] - pixel))
    surface.blit(stroke, (pos[0] + pixel, pos[1] - pixel))
    surface.blit(stroke, (pos[0] - pixel, pos[1] + pixel))
    surface.blit(stroke, (pos[0] + pixel, pos[1] + pixel))
    surface.blit(text, pos)

pygame.init()
pygame.mouse.set_visible(False)
cursor_img = pygame.image.load('textures\cursor.png').convert_alpha()
pygame.display.set_caption('ШАХТ МАЙНЕР')
clock = pygame.time.Clock()


f_stan = pygame.font.SysFont('sans serif', 36)
f0 = pygame.font.Font("textures/font/Rubik-Bold.ttf", 32)

f1 = pygame.font.Font("textures/font/Rubik-Bold.ttf", 24)

f2 = pygame.font.Font("textures/font/Rubik-Bold.ttf", 18)

f3 = pygame.font.Font("textures/font/Rubik-Bold.ttf", 16)

f4 = pygame.font.Font("textures/font/Rubik-Bold.ttf", 12)

orb_sound = pygame.mixer.Sound("sounds/orb.mp3")
crash_sound = pygame.mixer.Sound("sounds/crash.mp3")
music_cave = pygame.mixer.Sound("sounds/music.mp3")


class Titles:
    def __init__(self):
        self.y = -60
        self.x = 420
        self.titles = False
        self.delay = 120
        self.phrases = ['Cоздатель: Арсений Лаптев',
                        'Геймдизайнер: Арсений Лаптев', 'Программист: Арсений Лаптев',
                        'Музыка: из игры Dead Cells', 'Звуки: рандом сайты (хз если честно)', 'Диалоги: Арсений Лаптев',
                        'Другое: Арсений Лаптев', 'Тестеры: Константин Скобельцын', 'Тестеры: Даниил Лаптев',
                        'Тестеры: Артем Репин', 'Тестеры: Семен Красновский']

    def action(self):
        print('action')
        if self.y == 2140:
            self.titles = False
        if not self.titles:
            return
        print('поехали')
        draw_stroke(self.phrases[0], f0, sc, (self.x - len(self.phrases[0]) * 8, self.y), (255, 255, 255))
        draw_stroke(self.phrases[1], f0, sc, (self.x - len(self.phrases[1]) * 8, self.y - self.delay), (255, 255, 255))
        draw_stroke(self.phrases[2], f0, sc, (self.x - len(self.phrases[2]) * 8, self.y - self.delay * 2), (255, 255, 255))
        draw_stroke(self.phrases[3], f0, sc, (self.x - len(self.phrases[3]) * 8, self.y - self.delay * 3), (255, 255, 255))
        draw_stroke(self.phrases[4], f0, sc, (self.x - len(self.phrases[4]) * 8, self.y - self.delay * 4), (255, 255, 255))
        draw_stroke(self.phrases[5], f0, sc, (self.x - len(self.phrases[5]) * 8, self.y - self.delay * 5), (255, 255, 255))
        draw_stroke(self.phrases[6], f0, sc, (self.x - len(self.phrases[6]) * 8, self.y - self.delay * 6), (255, 255, 255))
        draw_stroke(self.phrases[7], f0, sc, (self.x - len(self.phrases[7]) * 8, self.y - self.delay * 7), (255, 255, 255))
        draw_stroke(self.phrases[8], f0, sc, (self.x - len(self.phrases[8]) * 8, self.y - self.delay * 8), (255, 255, 255))
        draw_stroke(self.phrases[9], f0, sc, (self.x - len(self.phrases[9]) * 8, self.y - self.delay * 9), (255, 255, 255))
        self.y += 1

titles = Titles()

class Inventory:
    def __init__(self):
        self.buying = pygame.mixer.Sound("sounds/buying.mp3")
        self.score = 0
        self.money = 0
        self.skin = 0
        self.y = -403
        self.kirka = True
        self.opening = False
        self.surface_kirka = pygame.Surface((400, 600), pygame.SRCALPHA, 32)
        self.surface_kirka = self.surface_kirka.convert_alpha()
        self.kirkabar1 = pygame.image.load('textures/pickaxe_wood.png').convert_alpha()
        self.kirkabar2 = pygame.image.load('textures/pickaxe_stone.png').convert_alpha()
        self.kirkabar3 = pygame.image.load('textures/pickaxe_copper.png').convert_alpha()
        self.kirkabar4 = pygame.image.load('textures/pickaxe_stal.png').convert_alpha()
        self.kirkabar5 = pygame.image.load('textures/pickaxe_gold.png').convert_alpha()
        self.kirkabar6 = pygame.image.load('textures/pickaxe_emerald.png').convert_alpha()
        self.kirkabars = [self.kirkabar1, self.kirkabar2, self.kirkabar3, self.kirkabar4, self.kirkabar5, self.kirkabar6]
        self.kirkabars_sum = [520, 1140, 3100, 5450, 10350, 15000]
        # 10 30 100
        self.durability_num = [[5, 10, 75], [5, 8, 50], [3, 7, 20], [2, 5, 15], [1, 3, 8], [1, 2, 3]]
        # self.durability_num = [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]
        self.scorebar = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/scorebar.png').convert_alpha()

    def action(self):
        if self.opening:
            self.open()
        else:
            self.close()
        if self.kirka:
            self.surface_kirka.blit(self.scorebar, (0, 0))
            self.surface_kirka.blit(self.kirkabars[self.skin], (152, 90))
            self.show_score()
            self.show_money()
            self.show_skin_sum()
            fones.surface_shaht.blit(self.surface_kirka, (1500, self.y))

    def check(self, pos):
        if 275 <= pos[0] <= 335 and 275 <= pos[1] <= 295:
            self.opening = False
        elif 275 <= pos[0] <= 335 and 10 <= pos[1] <= 35:
            self.opening = True
        if 22 <= pos[1] <= 70 and 1512 <= pos[0] <= 1580 and self.opening and taskbar_klass.buy_ready and self.skin != 6:
            if self.kirkabars_sum[self.skin] <= self.money:
                self.money -= self.kirkabars_sum[self.skin]
                coal.durability = math.ceil(coal.durability / coal.durability_max * self.durability_num[self.skin][0])
                copper.durability = math.ceil(copper.durability / copper.durability_max * self.durability_num[self.skin][1])
                iron.durability = math.ceil(iron.durability / iron.durability_max * self.durability_num[self.skin][2])
                coal.durability_max, copper.durability_max, iron.durability_max = self.durability_num[self.skin]
                self.buying.play()
                self.skin += 1

    def open(self):
        if self.y != 0:
            self.y += 31

    def close(self):
        if self.y != -403:
            self.y -= 31

    def show_money(self):
        draw_stroke(str(self.money), f2, self.surface_kirka, (159, 300), (255, 255, 0))

    def show_score(self):
        draw_stroke(str(self.score), f2, self.surface_kirka, (159, 350), (255, 255, 255))

    def show_skin_sum(self):
        if self.skin == 5:
            name = '-'
        else:
            name = str(self.kirkabars_sum[self.skin])
        draw_stroke(name, f3, self.surface_kirka, (38, 49), (255, 255, 0))


class Stan:
    def __init__(self):
        self.play = True
        self.x = 1920
        self.y = 580
        self.animation = True
        self.phrases = ''
        self.length = 0
        self.count = -1
        self.do = False
        self.stan_animation = 1
        self.lkm = pygame.image.load('textures/lkm.png').convert_alpha()
        self.stan_image = pygame.image.load('textures/stan.png').convert_alpha()
        self.write_task = pygame.mixer.Sound("sounds/write_task.mp3")
        self.rect = self.stan_image.get_rect()

    def update(self):
        self.x -= 10
        if self.x <= 1410:
            self.count += 1
            self.animation = False

    def update_out(self):
        self.x += 10
        if self.x >= 1920:
            self.write_task.play()
            self.do = True
            if self.play:
                self.play = False
            taskbar_klass.task_statement = False
            taskbar_klass.act = True
            self.animation = True
            self.stan_animation = 1
            helper.task_help = True

    def text(self):
        if self.count == -1 and self.animation:
            return
        fones.surface_shaht.blit(self.lkm, (self.x - 15, self.y + 320))
        textRect = pygame.Rect(1000, 902, 400, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(fones.surface_shaht, self.phrases[self.count], (0, 0, 0), drawTextRect, f_stan, True)

        textRect = pygame.Rect(1002, 900, 400, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(fones.surface_shaht, self.phrases[self.count], (0, 0, 0), drawTextRect, f_stan, True)

        textRect = pygame.Rect(1000, 900, 400, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(fones.surface_shaht, self.phrases[self.count], (255, 255, 255), drawTextRect, f_stan, True)

    def action(self, phrases):
        print(taskbar_klass.task_num, self.count)
        self.length = len(phrases)
        self.phrases = phrases
        if self.animation:
            fones.surface_shaht.blit(self.stan_image, (self.x, self.y))
            if self.stan_animation == 1:
                stan.update()
            elif self.stan_animation == 2:
                stan.update_out()
        else:
            fones.surface_shaht.blit(self.stan_image, (self.x, self.y))
            stan.text()
        if self.do:
            if taskbar_klass.task_num == 1 and self.count == 4:
                taskbar_klass.buy_ready = True
            elif taskbar_klass.task_num == 3 and self.count == 4:
                fones.brush = True
            elif taskbar_klass.task_num == 4 and self.count == 5:
                fones.shaht_break = True
                fones.time2 = 50
            elif taskbar_klass.task_num == 4 and self.count == 7:
                fones.countdown = True
                taskbar_klass.time_seconds = 180
            elif taskbar_klass.task_num == 5 and self.count == 0:
                fones.shaht_break = False
            elif taskbar_klass.task_num == 5 and self.count == 4:
                fones.end = True
            elif taskbar_klass.task_num == 6 and self.count == 0:
                fones.shaht_break = False
                fones.time2 = 1
            elif taskbar_klass.task_num == 6 and self.count == 4:
                fones.end = True

    def check(self):
        if self.count < self.length - 1 and not self.animation:
            self.count += 1
        else:
            self.play = True
            self.animation = True
            self.count = -1
            self.stan_animation = 2



class Ore_mine:
    def __init__(self, image, durability, position, rare=0.125, score=1, key='q'):
        self.score = score
        self.image = image
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.position = position
        self.rect = self.image.get_rect(topleft=self.position)
        self.key = key
        self.durability = self.durability_max = durability
        self.rare = rare
        self.time_partikles = 10
        self.time_partikles_end = 10
        self.partikles_end_y = 0
        self.partikles = pygame.transform.scale(pygame.image.load('textures/partikles0.png').convert_alpha(), (250, 250))
        self.partikles2 = pygame.transform.scale(pygame.image.load('textures/partikles0.png').convert_alpha(), (250, 250))
        self.klass_kg = 0
        self.partikles_active = False

    def click(self):
        if helper.coal_help:
            helper.x += 300
            helper.coal_help = False
            helper.begin = True
        self.time_partikles = 10
        crash_sound.play()
        if self.durability > 1:
            self.durability -= 1
        else:
            inventory.score += self.score
            orb_sound.play()
            self.partikles_active = True
            self.durability = self.durability_max
            self.klass_kg += random.randint(1, 4) * self.rare
            self.klass_kg = round(self.klass_kg, 3)

    def update(self):
        self.rect.x -= 10
        if self.rect.left <= -520:
            global stan_animation
            stan_animation = False
            self.rect.right = 0

    def partikles_end(self):
        print('привет')
        if 0 < self.time_partikles_end <= 10:
            print('привет2')
            # sc.blit(partikles, (100, 100))
            self.partikles2.set_alpha(25 * self.time_partikles_end)
            image = pygame.transform.scale(self.image, (180, 180))
            image.set_alpha(25 * self.time_partikles_end)
            fones.surface_shaht.blit(self.partikles2, (self.position[0] - 20, self.position[1] - 25 + self.partikles_end_y))
            self.time_partikles_end -= 1
            self.partikles_end_y += 20
        else:
            self.time_partikles_end = 10
            self.partikles_end_y = 0
            self.partikles_active = False

    def show_duraility(self):
        textRect = pygame.Rect(self.position[0] + 30, self.position[1] + 200, 400, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(fones.surface_shaht, str(self.durability) + '/' + str(self.durability_max), (255, 255, 255), drawTextRect, f1, True)

    def check(self, pos):
        if self.rect.left <= pos[0] <= self.rect.right and self.rect.top <= pos[1] <= self.rect.bottom:
            self.click()
        else:
            return

    def action(self):
        if self.partikles_active:
            self.partikles_end()
        elif 0 < self.time_partikles <= 10:
            # sc.blit(partikles, (100, 100))
            self.partikles.set_alpha(20 * self.time_partikles)
            fones.surface_shaht.blit(self.partikles, (self.position[0] - 20, self.position[1] - 25))
            self.time_partikles -= 1
            image = pygame.transform.scale(self.image, (180, 180))
            fones.surface_shaht.blit(image, (self.position[0] + 10, self.position[1] + 10))
        else:
            fones.surface_shaht.blit(self.image, self.rect)
        if ore_klass.coal:
            coal.show_duraility()
        if ore_klass.copper:
            copper.show_duraility()
        if ore_klass.iron:
            iron.show_duraility()



class Taskbar:
    def __init__(self):
        self.y = -260
        self.sell_success = pygame.mixer.Sound("sounds/sell_success.mp3")
        self.sell_fail = pygame.mixer.Sound("sounds/sell_fail.mp3")
        self.kg_of_coal = coal.klass_kg
        self.kg_of_coal_max = 7
        self.kg_of_copper = copper.klass_kg
        self.kg_of_copper_max = 4
        self.kg_of_copper = iron.klass_kg
        self.kg_of_iron_max = 3.5
        self.kg_of_order_max = [20, 12]
        self.kg_of_tonncoal_max = 150
        self.task_of_game = ['Начало карьеры', 'Твердая медь', 'Копай железо пока...', 'Электроника',
                             'Большой куш - большие проблемы', 'Продолжение следует', 'Продолжение следует']
        self.task_statement = True
        self.time_seconds = 0
        self.delay = 0
        self.task_num = 0
        self.opening = False
        self.act = True
        self.buy_ready = False
        self.task = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/taskbar.png')
        # self.task = pygame.transform.scale(self.task, (450, 300))
        self.surface_task = pygame.Surface((450, 300), pygame.SRCALPHA, 32)
        self.surface_task = self.surface_task.convert_alpha()

    def task_change(self, num=1):
        self.task_statement = True
        self.task_num += num

    def task_activate(self):
        if self.task_statement:
            stan.action(phrase_collection[self.task_num])

    def get_coal(self):
        self.show_task_name(f'Добыть {self.kg_of_coal_max} кг угля.')
        self.show_task_progress(f'{self.kg_of_coal} кг / {self.kg_of_coal_max} кг')
        self.show_task_reward('450 далларов')

    def get_copper(self):
        self.show_task_name(f'Добыть {self.kg_of_copper_max} кг меди.')
        self.show_task_progress(f'{self.kg_of_copper} кг / {self.kg_of_copper_max} кг')
        self.show_task_reward('960 далларов')

    def get_iron(self):
        self.show_task_name(f'Добыть {self.kg_of_iron_max} кг железа.')
        self.show_task_progress(f'{self.kg_of_iron} кг / {self.kg_of_iron_max} кг')
        self.show_task_reward('2620 далларов')

    def get_to_combinat(self):
        self.show_task_name(f'Выполнить заказ')
        self.show_task_progress(f'{self.kg_of_copper} кг / {self.kg_of_order_max[0]} кг  {self.kg_of_iron} кг / {self.kg_of_order_max[1]} кг')
        self.show_task_reward('4200 далларов')

    def get_tonn_coal(self):
        self.show_task_name(f'Выполнить заказ')
        self.show_task_progress(f'{round(self.kg_of_coal / 1000, 3)} т / {self.kg_of_tonncoal_max / 1000} т')
        self.show_task_reward('9100 далларов')
        if self.time_seconds and self.task_num != 5:
            print(self.delay)
            self.time_clock()

    def time_clock(self):
        if self.time_seconds >= 60:
            draw_stroke(str(self.time_seconds // 60).rjust(2, '0') + ':' + str(self.time_seconds % 60).rjust(2, '0'), f1, self.surface_task, (300, 95))
        elif self.time_seconds != 0:
            if self.time_seconds % 2 == 1:
                draw_stroke(str(self.time_seconds // 60).rjust(2, '0') + ':' + str(
                    self.time_seconds % 60).rjust(2, '0'), f1, self.surface_task, (300, 95))
            else:
                draw_stroke(str(self.time_seconds // 60).ljust(2, '0') + ':' + str(
                    self.time_seconds % 60).rjust(2, '0'), f1, self.surface_task, (300, 95), (255, 0, 0))

        # self.time_seconds = 65
        if self.time_seconds and self.delay == 0:
            self.delay = 60
            self.time_seconds -= 1
        self.delay -= 1

    def show_task_name(self, name):
        draw_stroke(name, f1, self.surface_task, (70, 95))

    def show_task_progress(self, name):
        draw_stroke(name, f3, self.surface_task, (70, 135), pixel=1)

    def show_task_reward(self, name):
        draw_stroke(name, f2, self.surface_task, (110, 220), (255, 255, 0))

    def action(self):
        self.kg_of_coal = coal.klass_kg
        self.kg_of_copper = copper.klass_kg
        self.kg_of_iron = iron.klass_kg
        if self.opening:
            self.open()
        else:
            print('конец')
            self.close()
        fones.surface_shaht.blit(self.surface_task, (86, self.y))
        self.surface_task.blit(self.task, (0, 0))
        if not self.task_statement:
            if len(self.task_of_game[self.task_num]) >= 22:
                f = f2
            elif len(self.task_of_game[self.task_num]) >= 15:
                f = f1
            else:
                f = f0
            draw_stroke(self.task_of_game[self.task_num], f, self.surface_task, (55, 45), (0, 255, 0))
        if self.task_of_game[self.task_num] == 'Начало карьеры' and not self.task_statement:
            ore_klass.coal = True
            self.get_coal()
            if taskbar_klass.kg_of_coal >= taskbar_klass.kg_of_coal_max:
                if self.act:
                    self.task_change()
                    coal.klass_kg -= 7
                    coal.klass_kg = round(coal.klass_kg, 3)
                    inventory.money += 450
                    inventory.score += 100
                    self.act = False
        if self.task_of_game[self.task_num] == 'Твердая медь' and not self.task_statement:
            ore_klass.copper = True
            self.get_copper()
            if self.kg_of_copper >= self.kg_of_copper_max:
                if self.act:
                    copper.klass_kg -= 4
                    copper.klass_kg = round(copper.klass_kg, 3)
                    inventory.money += 960
                    inventory.score += 300
                    self.task_change()
                    self.act = False
        if self.task_of_game[self.task_num] == 'Копай железо пока...' and not self.task_statement:
            ore_klass.iron = True
            self.get_iron()
            if self.kg_of_iron >= self.kg_of_iron_max:
                if self.act:
                    iron.klass_kg -= 3.5
                    iron.klass_kg = round(iron.klass_kg, 3)
                    inventory.money += 2620
                    inventory.score += 750
                    self.task_change()
                    self.act = False
        if self.task_of_game[self.task_num] == 'Электроника' and not self.task_statement:
            self.get_to_combinat()
            if self.kg_of_copper >= self.kg_of_order_max[0] and self.kg_of_iron >= self.kg_of_order_max[1]:
                if self.act:
                    copper.klass_kg -= 20
                    copper.klass_kg = round(copper.klass_kg, 3)
                    iron.klass_kg -= 12
                    iron.klass_kg = round(iron.klass_kg, 3)
                    inventory.money += 4700
                    inventory.score += 1500
                    self.task_change()
                    self.act = False
        if self.task_of_game[self.task_num] == 'Большой куш - большие проблемы' and not self.task_statement:
            self.get_tonn_coal()
            if self.kg_of_coal >= self.kg_of_tonncoal_max:
                if self.act:
                    coal.klass_kg -= 150
                    coal.klass_kg = round(copper.klass_kg, 3)
                    inventory.money += 9100
                    inventory.score += 3500
                    self.task_change()
                    self.act = False
            elif self.time_seconds == 0:
                if self.act:
                    coal.klass_kg = 0
                    copper.klass_kg = 0
                    iron.klass_kg = 0
                    fones.grohot_end.play()
                    self.act = False
                    fones.time2 = 0
                    fones.bad_end = True

    def check(self, pos):
        if 275 <= pos[0] <= 335 and 275 <= pos[1] <= 295:
            self.opening = False
        if 275 <= pos[0] <= 335 and 10 <= pos[1] <= 35:
            if helper.task_help:
                helper.task_help = False
                helper.coal_help = True
            self.opening = True
        else:
            helper.buy_help = False
            if 726 <= pos[0] <= 738 and 192 <= pos[1] <= 204 and self.opening and ore_klass.coal:
                if coal.klass_kg >= 1:
                    self.sell_success.play()
                    coal.klass_kg -= 1
                    coal.klass_kg = round(coal.klass_kg, 3)
                    inventory.money += random.randint(12, 24) #18
                else:
                    self.sell_fail.play()
            elif 926 <= pos[0] <= 938 and 192 <= pos[1] <= 204 and self.opening and ore_klass.copper:
                if copper.klass_kg >= 1:
                    self.sell_success.play()
                    copper.klass_kg -= 1
                    copper.klass_kg = round(copper.klass_kg, 3)
                    inventory.money += random.randint(20, 74) #42
                else:
                    self.sell_fail.play()

            elif 1126 <= pos[0] <= 1138 and 192 <= pos[1] <= 204 and self.opening and ore_klass.copper:
                if iron.klass_kg >= 1:
                    self.sell_success.play()
                    iron.klass_kg -= 1
                    iron.klass_kg = round(iron.klass_kg, 3)
                    inventory.money += random.randint(72, 80) #72
                else:
                    self.sell_fail.play()
    def open(self):
        if self.y != 0:
            self.y += 20

    def close(self):
        if self.y != -260:
            self.y -= 20


class Ore:
    def __init__(self):
        self.y = -260
        self.coal = False
        self.opening = False

        self.time1 = 30
        self.time2 = 30
        self.time3 = 30

        self.surface_ore = pygame.Surface((1000, 400), pygame.SRCALPHA, 32)
        self.surface_ore = self.surface_ore.convert_alpha()
        self.coalbar = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/coalscore.png').convert_alpha()
        self.coalbar = pygame.transform.scale(self.coalbar, (200, 200))
        self.copper = False
        self.copperbar = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/copperscore.png').convert_alpha()
        self.copperbar = pygame.transform.scale(self.copperbar, (200, 200))

        self.ironbar = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/ironscore.png').convert_alpha()
        self.ironbar = pygame.transform.scale(self.ironbar, (200, 200))
        self.iron = False
        self.export = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/export.png').convert_alpha()
        self.export = pygame.transform.scale(self.export, (125, 57))
        # self.export = pygame.transform.scale(self.export, (200, 45))

    def action(self):
        if self.opening:
            ore_klass.open()
        else:
            ore_klass.close()
        if taskbar_klass.task_num > 1:
            if self.time2 != 0:
                self.time2 -= 1
            self.surface_ore.blit(self.export, (260, 170 - self.time2 * 2))
            draw_stroke('20 - 74', f4, self.surface_ore, (290, 192 - self.time2 * 2), pixel=1)
        if taskbar_klass.task_num > 2:
            if self.time3 != 0:
                self.time3 -= 1
            self.surface_ore.blit(self.export, (460, 170 - self.time3 * 2))
            draw_stroke('72 - 80', f4, self.surface_ore, (490, 192 - self.time3 * 2), pixel=1)
        if self.coal:
            if taskbar_klass.buy_ready:
                if self.time1 != 0:
                    self.time1 -= 1
                self.surface_ore.blit(self.export, (60, 170 - self.time1 * 2))
                draw_stroke('12 - 24', f4, self.surface_ore, (90, 192 - self.time1 * 2), pixel=1)
            self.surface_ore.blit(self.coalbar, (0, 0))
            ore_klass.show_ore(taskbar_klass.kg_of_coal)
            fones.surface_shaht.blit(self.surface_ore, (600, self.y))
        if self.copper:
            self.surface_ore.blit(self.copperbar, (200, 0))
            ore_klass.show_ore(taskbar_klass.kg_of_copper, 200)
            fones.surface_shaht.blit(self.surface_ore, (600, self.y))
        if self.iron:
            self.surface_ore.blit(self.ironbar, (400, 0))
            ore_klass.show_ore(taskbar_klass.kg_of_iron, 400)
            fones.surface_shaht.blit(self.surface_ore, (600, self.y))

    def check(self, pos):
        if 275 <= pos[0] <= 335 and 275 <= pos[1] <= 295:
            self.opening = False
        if 275 <= pos[0] <= 335 and 10 <= pos[1] <= 35:
            self.opening = True
        else:
            return

    def open(self):
        if self.y != 0:
            self.y += 20

    def close(self):
        if self.y != -260:
            self.y -= 20

    def show_ore(self, massa, r=0):
        textRect = pygame.Rect(40 + r, 130, 200, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(self.surface_ore, str(massa) + ' кг', (0, 0, 0), drawTextRect, f2, True)


class Menu:
    def __init__(self):
        self.y = -510
        self.opening = False
        self.stop = False
        self.menu_off = True
        self.menu = pygame.image.load('textures/menu.png').convert_alpha()

    def check_play(self, pos):
        if 675 <= pos[0] <= 1305 and 332 <= pos[1] <= 442:
            self.stop = False
            self.opening = False
        else:
            return

    def check_save(self, pos):
        if 675 <= pos[0] <= 1305 and 488 <= pos[1] <= 598:
            self.opening = False
        else:
            return

    def check_headmenu(self, pos):
        if 675 <= pos[0] <= 1305 and 642 <= pos[1] <= 752:
            fones.check_headmenu((50, 900))
            self.opening = False
        else:
            return

    def action(self):
        if not self.stop:
            if self.opening:
                menu_klass.open()
            else:
                menu_klass.close()
        fones.surface_shaht.blit(self.menu, (469, self.y))

    def open(self):
        if self.y != 0:
            self.y += 30
        else:
            self.menu_off = False
            self.stop = True

    def close(self):
        if self.y != -1080:
            self.y -= 30
        else:
            self.menu_off = True
            self.stop = True


class Action:  # класс-администратор отвечающий на вызовы пользователя и вызывающий объекты
    def __init__(self):
        self.taskbar = False
        self.pickaxe = False
        self.coal = False
        self.money = False

    def taskbar_on(self):
        taskbar_klass.action()

    def coal_on(self):
        coal.action()

    def copper_on(self):
        copper.action()

    def iron_on(self):
        iron.action()

    def pickaxe_on(self):
        pickaxe.action()

    def ore_on(self):
        ore_klass.action()

    def menu_on(self):
        menu_klass.action()


class MainMenu:
    def __init__(self):
        self.y = 600
        self.menu_group = pygame.image.load('textures/menu_group.png').convert_alpha()
        self.logo = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/logo.png').convert_alpha()
        self.time = 0

    def action(self):
        fones.surface_mainmenu.blit(self.logo, (880, 0))
        self.menu_group.set_alpha(3 * self.time)
        fones.surface_mainmenu.blit(self.menu_group, (900, self.y))
        if self.y != 300:
            self.time += 1
            self.y -= 3



class Fone:
    def __init__(self):
        self.shaht_break = False
        self.bad_end = False
        self.shaht_sound = pygame.mixer.Sound("sounds/music.mp3")
        self.end_sound = pygame.mixer.Sound("sounds/to_be_continued.mp3")
        self.mainmenu_sound = pygame.mixer.Sound("sounds/mainmenu.mp3")
        self.chain = pygame.mixer.Sound("sounds/chain.mp3")
        self.y = 4320
        self.y2 = 0
        self.end = False
        self.y_delta = 1080
        self.y_delta2 = 2160
        self.y_delta3 = 3240
        self.bg = pygame.image.load('textures/shaht.jpg')
        self.surface_shaht = pygame.Surface((1920, 1080))
        self.surface_mainmenu = pygame.Surface((1920, 1080))
        self.surface_titles = pygame.Surface((1920, 1080))
        self.time_to_back = True
        self.bg2 = pygame.image.load('textures/headmenu.jpg')

        self.bg_delta = pygame.image.load('textures/delta.jpg')
        self.change = False
        self.in_headmenu = True
        self.in_shaht = False
        self.in_shop = False
        self.in_furnace = False
        self.in_ability = False
        self.opening = False
        self.black_bg = pygame.Surface((1920, 1080))
        self.black_bg.fill((0, 0, 0))

        self.position_headmenu_icon = [20, 920]
        self.position_shaht_icon = [20, 1000]
        self.position_brush_icon = [20, 1080]
        self.intro_seconds = 51
        self.time = 0
        self.time2 = 0
        self.speed = 50
        self.delay = 51
        self.time_delay = 100
        self.time3 = 0
        self.countdown = False
        self.change2 = False
        self.change3 = False
        self.brush = False
        self.start = True
        self.to = True
        self.logo_mp3_activate = True
        self.delay_start = False
        self.logo_mp3 = pygame.mixer.Sound("sounds/logo.mp3")
        self.grohot_end = pygame.mixer.Sound("sounds/grohot_end.mp3")
        self.grohot = pygame.mixer.Sound("sounds/grohot.mp3")
        self.headmenu_icon = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/headmenu-icon.png').convert_alpha()
        self.shaht_icon = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/shaht-icon.png').convert_alpha()
        self.brush_icon = pygame.image.load(f'textures/skins/{skins.skin[skins.num]}/brush-icon.png').convert_alpha()
        self.blacksun = pygame.image.load('textures/blacksun.png').convert_alpha()
        self.blacksun_logo = pygame.image.load('textures/logo Blacksun.png').convert_alpha()
        # self.shop_icon = pygame.image.load('shop-icon.png').convert_alpha()
        # self.furnace_icon = pygame.image.load('furnace-icon.png').convert_alpha()
        # self.ability_icon = pygame.image.load('ability-icon.png').convert_alpha()
        self.surf_black = pygame.Surface((1920, 1080))

    def check(self, pos):
        self.check_headmenu(pos)
        self.check_shaht(pos)


    def check_headmenu(self, pos):
        if self.position_headmenu_icon[0] <= pos[0] <= self.position_headmenu_icon[0] + 64 \
                and self.position_headmenu_icon[1] <= pos[1] <= self.position_headmenu_icon[1] + 64 and not (self.change or self.change2):
            self.change2 = True
            self.chain.play()
            self.time = 8
            main_menu_klass.y = 600
            main_menu_klass.times = 0
        else:
            return

    def check_shaht(self, pos):
        if self.position_shaht_icon[0] <= pos[0] <= self.position_shaht_icon[0] + 64 \
                and self.position_shaht_icon[1] <= pos[1] <= self.position_shaht_icon[1] + 64 and not (self.change or self.change2):
            self.change = True
            self.chain.play()
            self.time = 8
        else:
            return

    def action(self):
        if self.change2:
            if self.y2 == -4269:
                self.mainmenu_sound.set_volume(1)
                self.shaht_sound.set_volume(0.5)
                self.end_sound.set_volume(0.5)
                self.mainmenu_sound.play(loops=-1)
            if self.y2 == -1000:
                self.shaht_sound.set_volume(0.2)
                self.end_sound.set_volume(0.2)
            if self.y_delta >= 8:
                self.in_headmenu = True
                self.in_shaht = False
            if self.y2 == 0:
                self.shaht_sound.stop()
                self.change2 = False
                self.speed = 50
            else:
                self.y += self.speed
                self.y2 += self.speed
                self.y_delta += self.speed
                self.y_delta3 += self.speed
                self.y_delta2 += self.speed
                if self.speed != 8:
                    self.speed -= 1
            sc.blit(self.bg_delta, (0, self.y_delta))
            sc.blit(self.surface_titles, (0, self.y_delta2))
            self.surface_titles.blit(self.bg_delta, (0, 0))

            sc.blit(self.bg_delta, (0, self.y_delta3))

        if self.in_shaht:
            print('time', self.time2)
            if self.bad_end and self.time_to_back:
                sc.blit(self.surface_shaht, (0, random.randint(-2, 2)))
            if self.shaht_break:
                if self.countdown or self.time2 == 49 or self.time2 == 48:
                    self.time2 -= 1
            if 0 < self.time2 <= 50 and self.shaht_break:
                if self.time2 == 49:
                    self.grohot.play()
                sc.blit(self.surface_shaht, (random.randint(-1, 1), random.randint(-1, 1)))
            else:
                sc.blit(self.surface_shaht, (0, self.y))
            self.surface_shaht.blit(self.bg, (0, 0))
            if self.time2 == 1:
                self.time2 = random.randint(0 + taskbar_klass.time_seconds // 2, 100 + taskbar_klass.time_seconds)
        if self.change:
            if self.y2 == -50:
                if self.end:
                    self.end_sound.play()
                    self.end_sound.set_volume(1)
                else:
                    self.shaht_sound.play(loops=-1)
                    self.shaht_sound.set_volume(1)
                self.mainmenu_sound.set_volume(0.5)
            if self.y2 <= -3287:
                self.mainmenu_sound.set_volume(0.2)
            if self.y_delta3 <= 9:
                self.in_headmenu = False
                self.in_shaht = True
            if self.y2 == -4319:

                self.mainmenu_sound.stop()
                self.change = False
                self.speed = 50
            else:
                self.y -= self.speed
                self.y2 -= self.speed
                self.y_delta -= self.speed
                self.y_delta2 -= self.speed
                self.y_delta3 -= self.speed
                if self.speed != 8:
                    self.speed -= 1
            sc.blit(self.bg_delta, (0, self.y_delta))

            sc.blit(self.surface_titles, (0, self.y_delta2))
            self.surface_titles.blit(self.bg_delta, (0, 0))
            if not helper.begin:
                self.surface_titles.blit(self.blacksun, (486, 420))

            sc.blit(self.bg_delta, (0, self.y_delta3))

        if self.in_headmenu:
            sc.blit(self.surface_mainmenu, (0, self.y2))
            self.surface_mainmenu.blit(self.bg2, (0, 0))
        self.icons()
        if self.bad_end:
            print('tfbgdfgfgfdgdfgfgdgd', 'ddddddddddddddddddddddddddddg', self.time3, 5 * self.time3)
            self.black_bg.set_alpha(self.time3)
            sc.blit(self.black_bg, (0, 0))
            if self.time3 < 255 and self.time_to_back:
                self.time3 += 1
            elif self.time3 != 0:
                self.time_to_back = False
                self.time3 -= 1
            else:
                taskbar_klass.task_change(2)
                self.bad_end = False


    def icons(self):
        if self.brush and self.position_brush_icon[1] != 1000:
            self.position_headmenu_icon[1] -= 2
            self.position_shaht_icon[1] -= 2
            self.position_brush_icon[1] -= 2

        if 0 < self.time <= 8 and self.change3 and self.brush:
            if self.time <= 4:
                brush_icon = pygame.transform.scale(self.brush_icon, (64 - self.time * 2, 64 - self.time * 2))
                sc.blit(brush_icon, (self.position_brush_icon[0] + self.time,
                                        self.position_brush_icon[1] + self.time))
            else:
                brush_icon = pygame.transform.scale(self.brush_icon, (64 - (9 - self.time) * 2, 64 - (9 - self.time) * 2))
                sc.blit(brush_icon, (self.position_brush_icon[0] + (9 - self.time),
                                       self.position_brush_icon[1] + (9 - self.time)))
        else:
            sc.blit(self.brush_icon, (self.position_brush_icon))
        if 0 < self.time <= 8 and self.change2:
            if self.time <= 4:
                headmenu_icon = pygame.transform.scale(self.headmenu_icon, (64 - self.time * 2, 64 - self.time * 2))
                sc.blit(headmenu_icon, (self.position_headmenu_icon[0] + self.time,
                                        self.position_headmenu_icon[1] + self.time))
            else:
                headmenu_icon = pygame.transform.scale(self.headmenu_icon, (64 - (9 - self.time) * 2, 64 - (9 - self.time) * 2))
                sc.blit(headmenu_icon, (self.position_headmenu_icon[0] + (9 - self.time),
                                       self.position_headmenu_icon[1] + (9 - self.time)))
            self.time -= 1
        else:
            sc.blit(self.headmenu_icon, (self.position_headmenu_icon))
        if 0 < self.time <= 8 and self.change:
            if self.time <= 4:
                shaht_icon = pygame.transform.scale(self.shaht_icon, (64 - self.time * 2, 64 - self.time * 2))
                sc.blit(shaht_icon, (self.position_shaht_icon[0] + self.time,
                                        self.position_shaht_icon[1] + self.time))
            else:
                shaht_icon = pygame.transform.scale(self.shaht_icon, (64 - (9 - self.time) * 2, 64 - (9 - self.time) * 2))
                sc.blit(shaht_icon, (self.position_shaht_icon[0] + (9 - self.time),
                                        self.position_shaht_icon[1] + (9 - self.time)))
            self.time -= 1
        else:
            sc.blit(self.shaht_icon, (self.position_shaht_icon))

    def intro(self):
        if self.logo_mp3_activate:
            self.logo_mp3_activate = False
            self.logo_mp3.play()
        self.surf_black.fill((0, 0, 0))
        sc.blit(self.surf_black, (0, 0))
        print(self.intro_seconds, self.delay)
        self.blacksun_logo.set_alpha(5 * (51 - self.intro_seconds))
        if self.to and self.intro_seconds != 0:
            self.intro_seconds -= 1
        elif self.intro_seconds == 0:
            self.to = False
            self.intro_seconds += 1
        elif not self.delay_start and self.time_delay != 0:
            self.time_delay -= 1
        else:
            self.intro_seconds += 1
        if self.intro_seconds == 51:
            self.delay_start = True
        if self.delay_start:
            self.surf_black.set_alpha(5 * self.delay)
            self.delay -= 1
        if self.delay == 0:
            self.start = False
            self.mainmenu_sound.play(loops=-1)

        sc.blit(self.blacksun_logo, (703, 380))


class Skins:
    def __init__(self):
        self.skin = ['usual', 'shaht', 'kingdom']
        self.num = 0
        self.buy = ''

    def change_skin(self):
        if self.buy == 'usual':
            self.num = 1
        else:
            self.num = 2
    def brush_activate(self):
        pass


skins = Skins()
coal = Ore_mine(pygame.image.load('textures/coal.png').convert_alpha(), 10, (700, 400), 0.245, 1, 'q')
copper = Ore_mine(pygame.image.load('textures/copper.png').convert_alpha(), 30, (1000, 400), 10.185, 3, 'w')
iron = Ore_mine(pygame.image.load('textures/iron.png').convert_alpha(), 100, (1300, 400), 10.325, 5, 'e')
taskbar_klass = Taskbar()
stan = Stan()
action_klass = Action()
ore_klass = Ore()
menu_klass = Menu()
fones = Fone()
main_menu_klass = MainMenu()


phrases1 = ["Приветствую тебя в шахтерском деле! Можешь звать меня Стэн)",
            "Шахтейка старовата, покойный дед мне в карьер, и особо ресурсов здесь не накопаешь, но для новичка сгодится!",
            "Раз ты пришел в наше подземное царство, видимо ты горишь желанием подзаработать, не правда ли?",
            "Однако доверить добычу дорогих ценных ресурсов как алмазы и рубины, я тебе не могу",
            "Так или иначе, первым заданием я поручу тебе добыть 7 кг угля. Справишься?",
            "Вот и отлично! Помни, на шахте тому почет, у кого уголь на-гора течет!",
            "Хватай деревянную кирку и за работу!"]

phrases2 = ["Хо-хо! А ты быстро справился, мой юный друг. Как ты уже догадался в руде всегда случайное количество полезного ископаемого.",
            'Вот твои 450 "далларов" - именно так еще древние шахтеры называли свои денежные сбережения. ',
            'К слову, 100 далларов = 2,78 доллара = 205.4 рублей. Понимаю, не за этой кучкой денег ты сюда шел, но не всё сразу :)',
            "Что-ж, ближе к делу, добудь-ка мне 4 кг меди. Эта порода твердая, обычной киркой дается туго!",
            'Теперь после каждого задания с данной рудой ты можешь продавать товар "напрямую" на "рынке". ',
            'Докопай уголька и прикупи каменную кирку!']

phrases3 = ["А ты не плох! Поздравляю, держи честно заработанные 980 далларов",
            "Как ты заметил руда стоит на рынке всегда по разному, к примеру, у меди цена варьируется в разбросе 50-ти далларов!",
            "Ха-х, заодно проверишь свое красноречие с покупателями.",
            "Железо тверже меди. Зато содержит больше полезного ископаемого и стоит на рынке дороже!",
            'А еще совет: Запасись рудой побольше и оптом она будет стоить дороже. Удачи!',
            "Как добудешь 3.5 кг, возвращайся за зарплатой"]

phrases4 = ["Вижу ты подустал...Дела как сажа бела, да? Но не зря, все же 2620 далларов заработал",
            "Тут от одного молодого человека заказ поступил. Он с комбината по производству электроники",
            "Необходимо 20 кг меди и 12 железа. Обещал за все про все аж 4500 далларов",
            "На кону большая сумма, не оплошай :). Кстати, как насчет нового окружения",
            'Теперь тебе доступна "Покупка скинов окружения". Стоит дорого, однако бесплатно ты не почувствуешь себя...',
            '...заядлым копателем с набором "Каменная кладка" или дворцовым шахтером с набором "Королевская казна"',]

phrases5 = ["Супер! Покупатель доволен. Да и я доволен, ты молодец! Как говорится, в шахте с кайлом и лопатой, а дома за столом богатым",
            "Даже чаевые оставил - 500 далларов надбавкой. Но тут какой-то ещё один предприниматель нарисовался",
            "Ты только не падай, но для его завода требуется полтоhs cотни угля! Да-да, 150 кг! Уголёк – как золото: и блестит и ценится, до сих пор!",
            "Зато сумма будет такой, о которой ты и не мечтал - 9100 далларов",
            "Это последнее поручение. Считай, выполнишь этот заказ и ты автоматом квалифицируешься с новичка в бывалого",
            "После этого я тебя отправлю в другую шахту для добычи серебра и золота...Хе-хе, за работу, старина!",
            "Ой-о, это явно не к добру. Скорее, нужно уходить отсюда! Шахта рушится, видимо опоры не выдерживают...",
            "Эй, ты спятил? Тебе жить надоело? Что-ж, по моим рассчетам, камень мне под ноги, у тебя есть не более 5 минут. ",
            "Буду ждать тебя на поверхности!"]

phrases6_2 = ["Фу-х, эй, давай, приходи в себя, ну же! Тебе еще жить и жить, юный друг!",
            "Ох, шахтерский уголек от беды уберег! Прибежал бы я на помощь чуть позже и тебя бы погребло здесь на веки",
            "Ты давай поправляйся, у всех бывают неудачи, но больше так не рискуй, я не всегда буду рядом!",
            "---",
            "Раз ты дошел до сюда, то знай: ТЫ КРАСАВЧИК! РЕСПЕКТ И УВАЖУХА!",
            'Теперь ты удостоен звания бывалого и можешь покинуть шахту "Угольные раскопки" переходя в "Золотую жилу"',
            "Она тебя ждет в следующей части игры, которая выйдет когда создатель соберет донатом 5000 рублей.",
            "Кидайте ему на сбер или на киви. Однако игра не заканчивается, и ты можешь бесконечно копать и грести бабосики)",
            'А на этом все! Пока! Игру создал Арсений Лаптев (2021 год) под псевдонимом "Blacksun". Увидимся в 2 части!'
]
phrases6_1 = ["Да ладно, ты жив! Еще и с углем в придачу. Да такому умельцу и руку пожать можно!",
            "Кто не рискует, тот не пьет шампанское, так ведь? Что же, выжил и урвал свои даллары!",
            "А ведь еще немного, и уснул бы вечным сном под грудой камня. Хоть медаль за отвагу вручай!",
            "---",
            "Раз ты дошел до сюда, то знай: ТЫ КРАСАВЧИК! РЕСПЕКТ И УВАЖУХА!",
            'Теперь ты удостоен звания бывалого и можешь покинуть шахту "Угольные раскопки" переходя в "Золотую жилу"',
            "Она тебя ждет в следующей части игры, которая выйдет когда создатель соберет донатом 5000 рублей.",
            "Кидайте ему на сбер или на киви. Однако игра не заканчивается, и ты можешь бесконечно копать и грести бабосики)",
            'А на этом все! Пока! Игру создал Арсений Лаптев (2021 год) под псевдонимом "Blacksun". Увидимся в 2 части!']

phrase_collection = [phrases1, phrases2, phrases3, phrases4, phrases5, phrases6_1, phrases6_2]


class Helper:
    def __init__(self):
        self.hint11 = pygame.image.load('textures/hint1.png').convert_alpha()
        self.hint12 = pygame.image.load('textures/hint2.png').convert_alpha()

        self.hint21 = pygame.image.load('textures/hint21.png').convert_alpha()
        self.hint22 = pygame.image.load('textures/hint22.png').convert_alpha()
        self.hand = pygame.image.load('textures/hand.png').convert_alpha()
        self.hand = pygame.transform.scale(self.hand, (100, 100))
        self.task_help = False
        self.coal_help = False
        self.begin = False
        self.buy_help = True
        self.x = 765
        self.delay = 20
        self.hint_list = [self.hint11, self.hint12]
        self.hint_list2 = [self.hint21, self.hint22]
        self.hint_anim = 0

    def help(self):
        if self.x >= 1600:
            self.x = 2000
        if self.task_help:
            if self.begin:
                self.task_help = False
                self.coal_help = True
                self.delay = 20
            else:
                fones.surface_shaht.blit(self.hint_list[self.hint_anim], (282, 13))
                if self.delay == 0:
                    self.delay = 20
                    self.hint_anim = 1 if self.hint_anim == 0 else 0
                self.delay -= 1
        elif self.coal_help:
            fones.surface_shaht.blit(self.hint_list2[self.hint_anim], (self.x, 460))
            if self.delay == 0:
                self.delay = 20
                self.hint_anim = 1 if self.hint_anim == 0 else 0
            self.delay -= 1
        if taskbar_klass.buy_ready and taskbar_klass.task_num == 1 and self.buy_help:
            fones.surface_shaht.blit(self.hand, (726, 192))

class Cursor:
    def __init__(self):
        self.cursor_img = pygame.image.load('textures\cursor.png').convert_alpha()
        self.cursor_img2 = pygame.image.load('textures\cursor2.png').convert_alpha()
        self.cursor_img3 = pygame.image.load('textures\cursor3.png').convert_alpha()
        self.cursor_img4 = pygame.image.load('textures\cursor4.png').convert_alpha()
        self.cursor_img5 = pygame.image.load('textures\cursor5.png').convert_alpha()
        self.cursor_img6 = pygame.image.load('textures\cursor6.png').convert_alpha()
        self.time = 96
        self.cursor_list = [self.cursor_img, self.cursor_img2, self.cursor_img3, self.cursor_img4, self.cursor_img5,
                            self.cursor_img4, self.cursor_img3, self.cursor_img2, self.cursor_img]

    def active(self, pos):
        sc.blit(self.cursor_list[self.time // 12], (pos))
        self.time -= 1
        if self.time == 0:
            self.time = 96

cursor = Cursor()
helper = Helper()
inventory = Inventory()

while True:
    clock.tick(FPS)
    fones.action()
    if fones.in_headmenu:
        titles.action()
        main_menu_klass.action()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if fones.start:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    fones.start = False
                    fones.mainmenu_sound.play(loops=-1)
                    fones.logo_mp3.stop()

            if menu_klass.menu_off:
                '''ЧЕК СТЭН'''
                if event.type == pygame.MOUSEBUTTONUP and main_menu_klass.y == 300:
                    if event.button == 1:
                        fones.check(event.pos)

            if event.type == pygame.MOUSEBUTTONUP and main_menu_klass.y == 300:
                if event.button == 1:
                    if 895 <= event.pos[0] <= 1535 and 300 <= event.pos[1] <= 410:
                        fones.change = True
                        fones.chain.play()
                    if 895 <= event.pos[0] <= 1535 and 600 <= event.pos[1] <= 710:
                        titles.titles = True
                    if 895 <= event.pos[0] <= 1535 and 750 <= event.pos[1] <= 860:
                        exit()
                    print(event.pos)

    elif fones.in_shaht:
        # sc.blit(bg, (random.randint(-1, 1), random.randint(-1, 1)))
        # drawWindow()
        '''STAN'''
        taskbar_klass.task_activate()

        '''ЗАДАНИЕ'''
        if ore_klass.coal:
            action_klass.coal_on()
        if ore_klass.copper:
            action_klass.copper_on()
        if ore_klass.iron:
            action_klass.iron_on()
        inventory.action()

        '''ИНВЕНТАРЬ'''
        action_klass.taskbar_on()
        action_klass.ore_on()

        helper.help()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            '''ЧЕК МЕНЮ'''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_klass.menu_menu_off = False
                    menu_klass.stop = False
                    if menu_klass.opening:
                        menu_klass.opening = False
                    else:
                        menu_klass.menu_off = False
                        menu_klass.opening = True
            if menu_klass.menu_off:
                '''ЧЕК СТЭН'''
                if event.type == pygame.MOUSEBUTTONUP:
                    print(event.pos)
                    if taskbar_klass.task_statement and not stan.animation:
                        stan.check()
                        continue
                    else:
                        fones.check(event.pos)
                '''ЧЕК руда'''
                if not stan.play and stan.animation:
                    if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or (event.type == pygame.KEYDOWN and event.key in (pygame.K_q, pygame.K_w, pygame.K_e,  pygame.K_t)):
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            event_thing = event.pos
                        elif event.key == pygame.K_q:
                            event_thing = (760, 500)
                        elif event.key == pygame.K_w:
                            event_thing = (1080, 500)
                        elif event.key == pygame.K_e:
                            event_thing = (1400, 500)
                        elif event.key == pygame.K_t:
                            taskbar_klass.time_seconds -= 40
                        if ore_klass.coal:
                            coal.check(event_thing)
                        if ore_klass.copper:
                            copper.check(event_thing)
                        if ore_klass.iron:
                            iron.check(event_thing)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if inventory.kirka:
                            inventory.check(event.pos)
                        ore_klass.check(event.pos)
                        taskbar_klass.check(event.pos)
                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #         coal.click()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        menu_klass.check_play(event.pos)
                        menu_klass.check_headmenu(event.pos)
                        menu_klass.check_save(event.pos)
    action_klass.menu_on()
    cursor.active(pygame.mouse.get_pos())
    if fones.start:
        fones.intro()
    pygame.display.update()
