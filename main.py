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
    interrupt_controller = INTERRUPT_CONTROLLER()
    ppu = PPU(vram, interrupt_controller)
    hram = HRAM()
    mmu = MMU(ram, cartucho.mbc, timer,
              hram, joypad, interrupt_controller,
              ppu)
    cpu = CPU(mmu, timer)

    while True:
        tick = cpu.step()
        if tick is None:
            cpu.registers["pc"] -= 1
            opcode = cpu.fetch()
            print(f"0x{opcode:02x}")
            exit()
        ppu.tick(tick)

start()
