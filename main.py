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

timer.interrupter = interrupt_controller

joypad.interrupter = interrupt_controller


def handle_key_down(bit, map):
    joypad.handle_key_press(bit, map)


def handle_key_up(bit, map):
    joypad.handle_key_press(bit, map)


controller_map = {
    "up": [2, "dpad"],
    "down": [3, "dpad"],
    "right": [0, "dpad"],
    "left": [1, "dpad"],
    "q": [0, "action"],
    "w": [1, "action"],
    "e": [2, "action"],
    "r": [3, "action"]
}

def handle_event():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            call = controller_map.get(key)
            if call is not None:
                print("entrou no keydown")
                joypad.handle_key_press(call[0], call[1])
                joypad.interrupter.request_interrupt(4)

        elif event.type == pygame.KEYUP:
            key = pygame.key.name(event.key)
            call = controller_map.get(key)
            if call is not None:
                joypad.handle_key_press(call[0], call[1])
    
        elif event.type == pygame.QUIT:
            exit()


while rodando:
    tick = cpu.step()
    handle_event()
    if (interrupt_controller.IF >> 4) & 1 == 0 and (interrupt_controller.IE >> 4 & 1 == 1):
        print(f"{interrupt_controller.IF:08b}")
    if ppu.start_render:
        renderizar(ppu.display_buffer, screen)
        ppu.start_render = False

pygame.quit()
