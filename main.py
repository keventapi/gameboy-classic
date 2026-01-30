import time
import loader
from gameboy.memory.cartridge import CARTRIDGE
from gameboy.IO.timer import TIMER
from gameboy.IO.joypad import JOYPAD
from gameboy.cpus.cpu import CPU
from gameboy.cpus.interrupt_controller import INTERRUPT_CONTROLLER
from gameboy.cpus.mmu import MMU
from gameboy.memory.RAM import RAM, VRAM, HRAM
from gameboy.cpus.ppu import PPU
from gameboy.memory.OAM import OAM
import pygame


def load_rom(file_name):
    with open(file_name, "rb") as f:
        rom = f.read()
    return rom


pygame.init()
largura, altura = 160, 144
escala = 4 
screen = pygame.display.set_mode((largura * escala, altura * escala))
clock = pygame.time.Clock()


PALETA = {
    0: (155, 188, 15),
    1: (139, 172, 15),
    2: (48, 98, 48),
    3: (15, 56, 15)
}


def renderizar(buffer, screen):
    surface = pygame.Surface((160, 144))

    for y in range(144):
        for x in range(160):
            color_id = buffer[y][x]
            surface.set_at((x, y), PALETA[color_id])

    scaled_surface = pygame.transform.scale(surface, (160 * escala,
                                                      144 * escala))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()


rodando = True

game = loader.choose_game()
rom_bytes = load_rom(game)
ram = RAM()
cartucho = CARTRIDGE(rom_bytes)
interrupt_controller = INTERRUPT_CONTROLLER()
vram = VRAM()
oam = OAM()
ppu = PPU(vram, interrupt_controller, oam)
timer = TIMER(ppu)
joypad = JOYPAD()
hram = HRAM()
mmu = MMU(ram, cartucho.mbc, timer,
          hram, joypad, interrupt_controller,
          ppu)
timer.mmu = mmu
ppu.mmu = mmu
cpu = CPU(mmu, timer)


def handle_key(key, bit, map):
    jp_data = joypad.read()
    action = (jp_data >> 5) & 1
    dpad = (jp_data >> 4) & 1
    if map == "action" and not action:
        joypad.action[key] = ~(joypad.action[key])
    if map == "move" and not dpad:
        joypad.dpad[key] = ~(joypad.dpad[key])


controller_map = {
    "up": lambda: handle_key("up", 2, "move"),
    "down": lambda: handle_key("down", 3, "move"),
    "right": lambda: handle_key("right", 0, "move"),
    "left": lambda: handle_key("left", 1, "move"),
    "z": lambda: handle_key("A", 0, "action"),
    "x": lambda: handle_key("B", 1, "action"),
    "a": lambda: handle_key("start", 2, "action"),
    "s": lambda: handle_key("select", 3, "action")
}

while rodando:
    start_time = time.perf_counter()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            key = pygame.key.name(event.key)
            call = controller_map.get(key)
            if call is not None:
                call()

        if event.type == pygame.QUIT:
            rodando = False

    tick = cpu.step()
    if ppu.start_render:
        renderizar(ppu.display_buffer, screen)
        ppu.start_render = False


pygame.quit()
