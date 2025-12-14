import loader
from gameboy.memory.cartridge import CARTRIDGE
from gameboy.IO.timer import TIMER
from gameboy.cpus.cpu import CPU
from gameboy.cpus.mmu import MMU
from gameboy.memory.RAM import RAM, VRAM


def load_rom(file_name):
    with open(file_name, "rb") as f:
        rom = f.read()
    return rom


def start():
    game = loader.choose_game()
    rom_bytes = load_rom(game)
    ram = RAM()
    cartucho = CARTRIDGE(rom_bytes)
    timer = TIMER()
    vram = VRAM()
    mmu = MMU(ram, cartucho.mbc, timer, vram)
    cpu = CPU(mmu, timer)

    while True:
        cpu.step()


start()
