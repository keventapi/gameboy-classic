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
import numpy as np

class PROCESS:
    def __init__(self):
        self.frame_count = 0
        self.last_time = pygame.time.get_ticks()

        pygame.init()
        self.altura = 144
        self.largura = 160
        self.escala = 4
        self.screen = pygame.display.set_mode((self.largura * self.escala, self.altura * self.escala))
        self.clock = pygame.time.Clock()
        self.surface_gameboy = pygame.Surface((160, 144))
        self.scaled_size = (self.largura * self.escala, self.altura * self.escala)

        self.np_paleta = np.array([
            [255, 255, 255],
            [170, 170, 170],
            [85, 85, 85],
            [0, 0, 0]
        ], dtype=np.uint8)

        self.controller_map = {
            "up": [2, "dpad"],
            "down": [3, "dpad"],
            "right": [0, "dpad"],
            "left": [1, "dpad"],
            "q": [0, "action"],
            "w": [1, "action"],
            "e": [2, "action"],
            "r": [3, "action"]
        }
        self.start_gameboy()

    def start_gameboy(self):
        self.rodando = True
        self.game = loader.choose_game()
        self.rom_bytes = self.load_rom(self.game)
        self.ram = RAM()
        self.cartucho = CARTRIDGE(self.rom_bytes)
        self.interrupt_controller = INTERRUPT_CONTROLLER()
        self.vram = VRAM()
        self.oam = OAM()
        self.ppu = PPU(self.vram, self.interrupt_controller, self.oam)
        self.timer = TIMER(self.ppu)
        self.joypad = JOYPAD()
        self.hram = HRAM()
        self.mmu = MMU(self.ram, self.cartucho.mbc, self.timer, self.hram, self.joypad, self.interrupt_controller,self.ppu)
        self.timer.mmu = self.mmu
        self.ppu.mmu = self.mmu
        self.cpu = CPU(self.mmu, self.timer)
        self.timer.interrupter = self.interrupt_controller
        self.joypad.interrupter = self.interrupt_controller
        self.run()

    def load_rom(self, file_name):
        with open(file_name, "rb") as f:
            rom = f.read()
        return rom

    def renderizar(self, buffer, screen):
        ids = np.frombuffer(buffer, dtype=np.uint8).reshape((144, 160)) 
        rgb_array = self.np_paleta[ids]
        pygame.surfarray.blit_array(self.surface_gameboy, rgb_array.transpose(1, 0, 2))

        pygame.transform.scale(self.surface_gameboy, self.scaled_size, screen)
        pygame.display.flip()

    def handle_key_down(self, bit, map):
        self.joypad.handle_key_press(bit, map)

    def handle_key_up(self, bit, map):
        self.joypad.handle_key_press(bit, map)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                call = self.controller_map.get(key)
                if call is not None:
                    self.joypad.handle_key_press(call[0], call[1])
                    self.joypad.interrupter.request_interrupt(4)

            elif event.type == pygame.KEYUP:
                key = pygame.key.name(event.key)
                call = self.controller_map.get(key)
                if call is not None:
                    self.joypad.handle_key_press(call[0], call[1])

            elif event.type == pygame.QUIT:
                exit()

    def run(self):
        event_counter = 0 

        while self.rodando:
            tick = self.cpu.step()
            event_counter += tick
            if event_counter > 1000:
                self.handle_event()
                event_counter = 0

            if self.ppu.start_render:
                agora = pygame.time.get_ticks()
                if agora - self.last_time > 1000:
                    fps_real = self.frame_count
                    pygame.display.set_caption(f"GameBoy | FPS Real: {fps_real}")
                    self.frame_count = 0
                    self.last_time = agora
                self.renderizar(self.ppu.display_buffer, self.screen)
                self.ppu.start_render = False

                self.frame_count += 1


gb = PROCESS()
