import time
import loader
from gameboy.memory.cartridge import CARTRIDGE
from gameboy.IO.timer import TIMER
from gameboy.IO.joypad import JOYPAD
from gameboy.cpus.cpu import CPU
from gameboy.cpus.interrupt_controller import INTERRUPT_CONTROLLER
from gameboy.cpus.mmu import MMU
from gameboy.memory.RAM import RAM, VRAM, HRAM


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
    joypad = JOYPAD()
    vram = VRAM()
    hram = HRAM()
    interrupt_controller = INTERRUPT_CONTROLLER()
    mmu = MMU(ram, cartucho.mbc, timer, vram,
              hram, joypad, interrupt_controller)
    cpu = CPU(mmu, timer)

    while True:
        cpu.step()


start()
