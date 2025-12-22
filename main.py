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

    scaled_surface = pygame.transform.scale(surface, (160 * escala, 144 * escala))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()


rodando = True

game = loader.choose_game()
rom_bytes = load_rom(game)
ram = RAM()
cartucho = CARTRIDGE(rom_bytes)
timer = TIMER()
joypad = JOYPAD()
vram = VRAM()
interrupt_controller = INTERRUPT_CONTROLLER()
oam = OAM()
ppu = PPU(vram, interrupt_controller, oam)
hram = HRAM()
mmu = MMU(ram, cartucho.mbc, timer,
          hram, joypad, interrupt_controller,
          ppu)
ppu.mmu = mmu
cpu = CPU(mmu, timer)


while rodando:
    start_time = time.perf_counter()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    tick = cpu.step()
    if tick is None:
        tick = 4
    ppu.tick(tick)

    if ppu.start_render:
        renderizar(ppu.display_buffer, screen)
        ppu.start_render = False
        elapsed = time.perf_counter() - start_time
        sleep_time = (1/60.0) - elapsed
        if sleep_time > 0:
            print(sleep_time)
            time.sleep(sleep_time)

pygame.quit()
