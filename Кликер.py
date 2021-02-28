import pygame
import random
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

pygame.init()
pygame.mouse.set_visible(False)
cursor_img = pygame.image.load('textures\cursor.png').convert_alpha()
pygame.display.set_caption('ШАХТ МАЙНЕР')
clock = pygame.time.Clock()


f1 = pygame.font.SysFont('sans serif', 36)
f1_outline = pygame.font.SysFont('sans serif', 36)
f2 = pygame.font.SysFont('arial', 24)
f3 = pygame.font.SysFont('arial', 18)
orb_sound = pygame.mixer.Sound("sounds/orb.mp3")
crash_sound = pygame.mixer.Sound("sounds/crash.mp3")
music_cave = pygame.mixer.Sound("sounds/music.mp3")


class Inventory:
    def __init__(self):
        self.score = 0
        self.money = 0
        self.y = -325
        self.kirka = True
        self.opening = False
        self.surface_kirka = pygame.Surface((400, 600), pygame.SRCALPHA, 32)
        self.surface_kirka = self.surface_kirka.convert_alpha()
        self.kirkabar = pygame.image.load('textures/pickaxe_stal.png').convert_alpha()
        self.scorebar = pygame.image.load('textures/scorebar.png').convert_alpha()

    def action(self):
        if self.opening:
            self.open()
        else:
            self.close()
        if self.kirka:
            print('Я ТУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУУТ')
            self.surface_kirka.blit(self.scorebar, (0, 0))
            self.surface_kirka.blit(self.kirkabar, (85, 75))
            self.show_score()
            self.show_money()
            fones.surface_shaht.blit(self.surface_kirka, (1600, self.y))

    def check(self, pos):
        if 275 <= pos[0] <= 335 and 275 <= pos[1] <= 295:
            self.opening = False
        if 275 <= pos[0] <= 335 and 10 <= pos[1] <= 35:
            print('O P E N')
            self.opening = True
        else:
            return

    def open(self):
        if self.y != 0:
            self.y += 25

    def close(self):
        if self.y != -325:
            self.y -= 25

    def show_money(self):
        textRect = pygame.Rect(85, 220, 200, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(self.surface_kirka, str(self.money), (0, 0, 0), drawTextRect, f3, True)

    def show_score(self):
        textRect = pygame.Rect(85, 270, 200, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(self.surface_kirka, str(self.score), (0, 0, 0), drawTextRect, f3, True)


class Stan:
    def __init__(self):
        self.play = True
        self.x = 1920
        self.y = 580
        self.animation = True
        self.phrases = ''
        self.length = 0
        self.count = -1
        self.stan_animation = 1
        self.lkm = pygame.image.load('textures/lkm.png').convert_alpha()
        self.stan_image = pygame.image.load('textures/stan.png').convert_alpha()
        self.write_task = pygame.mixer.Sound("sounds/write_task.mp3")
        self.rect = self.stan_image.get_rect()

    def update(self):
        self.x -= 10
        # print(self.rect.left)
        if self.x <= 1410:
            self.count += 1
            self.animation = False

    def update_out(self):
        # print(self.rect.left)
        self.x += 10
        if self.x >= 1920:
            self.write_task.play()
            if self.play:
                self.play = False
            taskbar_klass.task_statement = False
            taskbar_klass.act = True
            self.animation = True
            self.stan_animation = 1
            helper.task_help = True

    def text(self):
        global f1_outline
        print('self.count-----------')
        if self.count == -1 and self.animation:
            return
        fones.surface_shaht.blit(self.lkm, (self.x - 15, self.y + 320))
        textRect = pygame.Rect(1000, 902, 400, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(fones.surface_shaht, self.phrases[self.count], (0, 0, 0), drawTextRect, f1_outline, True)

        textRect = pygame.Rect(1002, 900, 400, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(fones.surface_shaht, self.phrases[self.count], (0, 0, 0), drawTextRect, f1_outline, True)

        textRect = pygame.Rect(1000, 900, 400, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(fones.surface_shaht, self.phrases[self.count], (255, 255, 255), drawTextRect, f1_outline, True)

    def action(self, phrases):
        print(phrases, '----------------------------')
        self.length = len(phrases)
        self.phrases = phrases
        if self.animation:
            if self.stan_animation == 1:
                stan.update()
            elif self.stan_animation == 2:
                stan.update_out()
        fones.surface_shaht.blit(self.stan_image, (self.x, self.y))
        stan.text()

    def check(self):
        if self.count < self.length - 1:
            self.count += 1
            print('count', self.count)
        else:
            self.animation = True
            self.count = -1
            self.stan_animation = 2



class Ore_mine:
    def __init__(self, image, durability, position, rare=0.125, score=1):
        self.score = score
        self.image = image
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.position = position
        self.rect = self.image.get_rect(topleft=self.position)

        self.durability = self.durability_max = durability
        self.rare = rare
        self.time_partikles = 10
        self.partikles = pygame.transform.scale(pygame.image.load('textures/partikles0.png').convert_alpha(), (250, 250))
        self.klass_kg = 0

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
            self.durability = self.durability_max
            self.klass_kg += random.randint(1, 4) * self.rare
            self.klass_kg = round(self.klass_kg, 3)

    def update(self):
        self.rect.x -= 10
        # print(self.rect.left)
        if self.rect.left <= -520:
            global stan_animation
            stan_animation = False
            self.rect.right = 0


    def show_duraility(self):
        print(self.durability_max)
        textRect = pygame.Rect(self.position[0] + 30, self.position[1] + 200, 400, 300)
        drawTextRect = textRect.inflate(-5, -5)
        drawText(fones.surface_shaht, str(self.durability) + '/' + str(self.durability_max), (255, 255, 255), drawTextRect, f1, True)

    def check(self, pos):
        # print(self.rect.left, self.rect.right, self.rect.top, self.rect.bottom)
        if self.rect.left <= pos[0] <= self.rect.right and self.rect.top <= pos[1] <= self.rect.bottom:
            self.click()
        else:
            return

    def action(self):
        if 0 < self.time_partikles <= 10:
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
        self.kg_of_coal = coal.klass_kg
        self.kg_of_coal_max = 6
        self.kg_of_copper = copper.klass_kg
        self.kg_of_copper_max = 4
        self.kg_of_copper = iron.klass_kg
        self.kg_of_iron_max = 7
        self.kg_of_order_max = [20, 12]
        self.task_of_game = ['Добыть уголь 1', 'Добыть медь 2', 'Добыть железо 3', 'Заказ 4', 'Заказ 4']
        self.task_statement = True
        self.task_num = 0
        self.opening = False
        self.act = True
        self.task = pygame.image.load('textures/taskbar.png')
        self.task = pygame.transform.scale(self.task, (450, 300))
        self.surface_task = pygame.Surface((450, 300), pygame.SRCALPHA, 32)
        self.surface_task = self.surface_task.convert_alpha()

    def task_change(self):
        self.task_statement = True
        self.task_num += 1

    def task_activate(self):
        print('task_activatetask_activatetask_activatetask_activatetask_activatetask_activatetask_activate')
        if self.task_statement:
            stan.action(phrase_collection[self.task_num])

    def get_coal(self):
        self.show_task_name(f'Добыть {self.kg_of_coal_max} кг угля.')
        self.show_task_progress(f'{self.kg_of_coal} кг / {self.kg_of_coal_max} кг')
        self.show_task_reward('250 монет')

    def get_copper(self):
        print('copper')
        self.show_task_name(f'Добыть {self.kg_of_copper_max} кг меди.')
        self.show_task_progress(f'{self.kg_of_copper} кг / {self.kg_of_copper_max} кг')
        self.show_task_reward('720 монет')

    def get_iron(self):
        print('copper')
        self.show_task_name(f'Добыть {self.kg_of_iron_max} кг меди.')
        self.show_task_progress(f'{self.kg_of_iron} кг / {self.kg_of_iron_max} кг')
        self.show_task_reward('1620 монет')

    def get_to_combinat(self):
        print('copper')
        self.show_task_name(f'Добыть {self.kg_of_order_max[0]} кг меди, {self.kg_of_order_max[1]} кг железа.')
        self.show_task_progress(f'{self.kg_of_copper} кг / {self.kg_of_order_max[0]} кг  {self.kg_of_iron} кг / {self.kg_of_order_max[1]} кг')
        self.show_task_reward('1620 монет')

    def show_task_name(self, name):
        text = f2.render(name, True, (0, 0, 0))
        self.surface_task.blit(text, (70, 95))

    def show_task_progress(self, name):
        print('gfdgdfhgffdgfddhfgfd')
        text = f2.render(name, True, (0, 0, 0))
        self.surface_task.blit(text, (70, 125))

    def show_task_reward(self, name):
        text = f2.render(name, True, (0, 0, 0))
        self.surface_task.blit(text, (110, 220))

    def action(self):
        self.kg_of_coal = coal.klass_kg
        self.kg_of_copper = copper.klass_kg
        self.kg_of_iron = iron.klass_kg
        if self.opening:
            self.open()
        else:
            self.close()
        fones.surface_shaht.blit(self.surface_task, (86, self.y))
        self.surface_task.blit(self.task, (0, 0))

        if self.task_of_game[self.task_num] == 'Добыть уголь 1' and not self.task_statement:
            ore_klass.coal = True
            self.get_coal()
            if taskbar_klass.kg_of_coal >= taskbar_klass.kg_of_coal_max:
                if self.act:
                    self.task_change()
                    coal.klass_kg -= 6
                    coal.klass_kg = round(coal.klass_kg, 3)
                    inventory.money += 250
                    inventory.score += 100
                    self.act = False
        print(self.task_of_game[self.task_num] == 'Добыть медь 2', not self.task_statement, '------------')
        if self.task_of_game[self.task_num] == 'Добыть медь 2' and not self.task_statement:
            ore_klass.copper = True
            print(self.task_of_game[self.task_num])
            self.get_copper()
            if taskbar_klass.kg_of_copper >= taskbar_klass.kg_of_copper_max:
                if self.act:
                    copper.klass_kg -= 4
                    copper.klass_kg = round(copper.klass_kg, 3)
                    inventory.money += 720
                    inventory.score += 300
                    self.task_change()
                    self.act = False
        if self.task_of_game[self.task_num] == 'Добыть железо 3' and not self.task_statement:
            ore_klass.iron = True
            print(self.task_of_game[self.task_num])
            self.get_iron()
            if taskbar_klass.kg_of_iron >= taskbar_klass.kg_of_iron_max:
                if self.act:
                    iron.klass_kg -= 7
                    iron.klass_kg = round(iron.klass_kg, 3)
                    inventory.money += 1620
                    inventory.score += 750
                    self.task_change()
                    self.act = False
        if self.task_of_game[self.task_num] == 'Заказ 4' and not self.task_statement:
            print(self.task_of_game[self.task_num])
            self.get_to_combinat()
            if taskbar_klass.kg_of_copper >= taskbar_klass.kg_of_order_max[0] and taskbar_klass.kg_of_iron >= taskbar_klass.kg_of_order_max[1]:
                if self.act:
                    copper.klass_kg -= 20
                    copper.klass_kg = round(copper.klass_kg, 3)
                    iron.klass_kg -= 12
                    iron.klass_kg = round(iron.klass_kg, 3)
                    inventory.money += 4200
                    inventory.score += 4000
                    self.task_change()
                    self.act = False

    def check(self, pos):
        if 275 <= pos[0] <= 335 and 275 <= pos[1] <= 295:
            self.opening = False
        if 275 <= pos[0] <= 335 and 10 <= pos[1] <= 35:
            if helper.task_help:
                helper.task_help = False
                helper.coal_help = True
            self.opening = True
        else:
            return

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
        self.surface_ore = pygame.Surface((1000, 200), pygame.SRCALPHA, 32)
        self.surface_ore = self.surface_ore.convert_alpha()
        self.coalbar = pygame.image.load('textures/coalbar.png').convert_alpha()
        self.coalbar = pygame.transform.scale(self.coalbar, (200, 200))
        self.copper = False
        self.copperbar = pygame.image.load('textures/copperscore.png').convert_alpha()
        self.copperbar = pygame.transform.scale(self.copperbar, (200, 200))

        self.ironbar = pygame.image.load('textures/ironscore.png').convert_alpha()
        self.ironbar = pygame.transform.scale(self.ironbar, (200, 200))
        self.iron = False

    def action(self):
        if self.opening:
            ore_klass.open()
        else:
            ore_klass.close()

        if self.coal:
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
            print('O P E N')
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

    def check_headmenu(self, pos):
        if 675 <= pos[0] <= 1305 and 488 <= pos[1] <= 598:
            self.opening = False
        else:
            return

    def check_save(self, pos):
        if 675 <= pos[0] <= 1305 and 642 <= pos[1] <= 752:
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
        print('open')
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
        self.logo = pygame.image.load('textures/logo.png').convert_alpha()
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
        self.shaht_sound = pygame.mixer.Sound("sounds/music.mp3")
        self.mainmenu_sound = pygame.mixer.Sound("sounds/mainmenu.mp3")
        self.mainmenu_sound.play()
        self.chain = pygame.mixer.Sound("sounds/chain.mp3")
        self.y = 4320
        self.y2 = 0
        self.y_delta = 1080
        self.y_delta2 = 2160
        self.y_delta3 = 3240
        self.bg = pygame.image.load('textures/shaht.jpg')
        self.surface_shaht = pygame.Surface((1920, 1080))
        self.surface_mainmenu = pygame.Surface((1920, 1080))
        self.surface_titles = pygame.Surface((1920, 1080))

        self.bg2 = pygame.image.load('textures/headmenu.jpg')

        self.bg_delta = pygame.image.load('textures/delta.jpg')
        self.change = False
        self.in_headmenu = True
        self.in_shaht = False
        self.in_shop = False
        self.in_furnace = False
        self.in_ability = False
        self.opening = False
        self.position_headmenu_icon = 40, 900
        self.position_shaht_icon = 40, 980
        self.time = 0
        self.speed = 50
        self.change2 = False
        self.headmenu_icon = pygame.image.load('textures/headmenu-icon.png').convert_alpha()
        self.shaht_icon = pygame.image.load('textures/shaht-icon.png').convert_alpha()
        self.blacksun = pygame.image.load('textures/blacksun.png').convert_alpha()
        # self.shop_icon = pygame.image.load('shop-icon.png').convert_alpha()
        # self.furnace_icon = pygame.image.load('furnace-icon.png').convert_alpha()
        # self.ability_icon = pygame.image.load('ability-icon.png').convert_alpha()

    def check(self, pos):
        self.check_headmenu(pos)
        self.check_shaht(pos)


    def check_headmenu(self, pos):
        print('Проьбаааа')
        if self.position_headmenu_icon[0] <= pos[0] <= self.position_headmenu_icon[0] + 64 \
                and self.position_headmenu_icon[1] <= pos[1] <= self.position_headmenu_icon[1] + 64 and not (self.change or self.change2):
            self.change2 = True
            self.chain.play()
            self.time = 5
            main_menu_klass.y = 600
            main_menu_klass.times = 0
        else:
            return

    def check_shaht(self, pos):
        print('aaaffff')
        if self.position_shaht_icon[0] <= pos[0] <= self.position_shaht_icon[0] + 64 \
                and self.position_shaht_icon[1] <= pos[1] <= self.position_shaht_icon[1] + 64 and not (self.change or self.change2):
            print('ffff')
            self.chain.play()
            self.time = 5
            self.change = True
        else:
            return

    def action(self):
        if self.change2:
            print(self.y2, 'self.y2')
            if self.y2 == -4269:
                self.mainmenu_sound.set_volume(1)
                self.shaht_sound.set_volume(0.5)
                self.mainmenu_sound.play()
            if self.y2 == -1000:
                self.shaht_sound.set_volume(0.2)
            print('self.y_delta', self.y_delta)
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
            sc.blit(self.surface_shaht, (0, self.y))
            self.surface_shaht.blit(self.bg, (0, 0))
        if self.change:
            if self.y2 == -50:
                self.shaht_sound.play()
                self.shaht_sound.set_volume(1)
                self.mainmenu_sound.set_volume(0.5)
            if self.y2 <= -3287:
                self.mainmenu_sound.set_volume(0.2)
            print(self.y_delta3, 'delta3')
            if self.y_delta3 <= 9:
                self.in_headmenu = False
                self.in_shaht = True
            print(self.y2, 'y2')
            if self.y2 == -4319:
                print(self.y2)
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

    def icons(self):
        if 0 < self.time <= 5 and self.change2:
            self.time -= 1
            headmenu_icon = pygame.transform.scale(self.headmenu_icon, (48, 48))
            sc.blit(headmenu_icon, (self.position_headmenu_icon[0] + 8, self.position_headmenu_icon[1] + 8))
        else:
            sc.blit(self.headmenu_icon, (self.position_headmenu_icon))
        if 0 < self.time <= 5 and self.change:
            self.time -= 1
            shaht_icon = pygame.transform.scale(self.shaht_icon, (48, 48))
            sc.blit(shaht_icon, (self.position_shaht_icon[0] + 8, self.position_shaht_icon[1] + 8))
        else:
            sc.blit(self.shaht_icon, (self.position_shaht_icon))

stan = Stan()
coal = Ore_mine(pygame.image.load('textures/coal.png').convert_alpha(), 3, (700, 400), 0.125, 1)
copper = Ore_mine(pygame.image.load('textures/copper.png').convert_alpha(), 10, (1000, 400), 0.095, 3)
iron = Ore_mine(pygame.image.load('textures/iron.png').convert_alpha(), 18, (1300, 400), 0.215, 5)
taskbar_klass = Taskbar()
action_klass = Action()
ore_klass = Ore()
menu_klass = Menu()
fones = Fone()
main_menu_klass = MainMenu()


phrases1 = ["Приветствую тебя в шахтерском деле! Можешь звать меня Стэн)",
                        "Раз ты пришел в наше подземное царство, видимо ты горишь желанием подзаработать, не правда ли?",
                        "Однако доверить добычу дорогих ценных ресурсов как алмазы и рубины, я тебе не могу",
                        "Что-ж, первым заданием я поручу тебе добыть 6 кг угля. Справишься?",
                        "Вот и отлично! Уголь - порода обыденная, но незаменимая в плане топлива.",
                        "Хватай деревянную кирку и за работу!"]

phrases2 = ["Хо-хо! А ты быстро справился, мой юный друг. Вот твои 250 монет.",
            "Понимаю, не за этой кучкой денег ты сюда шел, но не всё сразу :)",
            "Теперь добудь-ка мне 4 кг меди. Эта порода твердая, деревянной киркой её не добыть!",
            "Покопай ещё угля и продай его оптом. Прикупи себе каменную кирку и вперёд!",
            ]

phrases3 = ["А ты не плох! Поздравляю, держи честно заработанные 720 монет",
            "Железо тверже меди. Однако с медной киркой добыть железо не составит проблем ",
            "Как добудешь 7 кг, возвращайся за зарплатой"]

phrases4 = ["Вижу ты подустал... Но не зря, все же 1620 монет заработал",
            "Тут от одного молодого человека заказ поступил. Он с комбината по производству электроники",
            "Необходимо 20 кг меди и 12 железа. Обещал за все про все аж 4200 монет",
            "На кону большая сумма, не оплошай :)"]

phrases5 = ["Супер! Покупатель доволен. Да и я доволен, ты молодец!",
            "Даже чаевые оставил - 500 монет надбавкой. Но тут ещё один предприниматель нарисовался",
            "Ты только не падай, но для его завода требуется тонна угля! Да-да, 1000 кг!",
            "Зато сумма будет такой, о которой ты и не мечтал - 12000 монет",
            "Это последнее поручение. Считай, выполнишь этот заказ и ты автоматом квалифицируешься с новичка в бывалого",
            "После этого я тебя отправлю в другую шахту для добычи серебра и золота...Хе-хе, за работу, старина!"]

phrase_collection = [phrases1, phrases2, phrases3, phrases4, phrases5]


class Helper:
    def __init__(self):
        self.hand = pygame.image.load('textures/hand.png').convert_alpha()
        self.hand = pygame.transform.scale(self.hand, (100, 100))
        self.task_help = False
        self.coal_help = False
        self.begin = False
        self.x = 765

    def help(self):
        if self.task_help:
            if self.begin:
                self.task_help = False
                self.coal_help = True
            fones.surface_shaht.blit(self.hand, (265, 10))
        elif self.coal_help:
            fones.surface_shaht.blit(self.hand, (self.x, 520))

helper = Helper()
inventory = Inventory()

while True:
    clock.tick(FPS)
    fones.action()
    if fones.in_headmenu:
        main_menu_klass.action()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
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
                    if 895 <= event.pos[0] <= 1535 and 750 <= event.pos[1] <= 860:
                        exit()
                    print(event.pos)

    elif fones.in_shaht:
        print('ПОНАРВАЛИ')
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
                    if taskbar_klass.task_statement:
                        stan.check()
                        continue
                    else:
                        fones.check(event.pos)
                '''ЧЕК руда'''
                if event.type == pygame.MOUSEBUTTONUP:
                    if (event.button == 1 or event.key == pygame.K_SPACE):
                        ore_klass.check(event.pos)
                        if inventory.kirka:
                            inventory.check(event.pos)
                        if ore_klass.coal:
                            coal.check(event.pos)
                        if ore_klass.copper:
                            copper.check(event.pos)
                        if ore_klass.iron:
                            iron.check(event.pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        print()
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
    sc.blit(cursor_img, (pygame.mouse.get_pos()))
    pygame.display.update()
