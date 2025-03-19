import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import os

class OpenRPG():
    IS_RUNNING: bool = False
    DATA_DIR: str = "./player/data"
    RESOLUTION: tuple = (640, 480)
    FPS: int = 60
    CHARSETS: list[str] = []
    TILESETS: list[str] = []
    MUSIC: list[str] = []
    NAME: str = ""
    SCREEN: pygame.Surface = None

    def load_charsets(self):
        for f in os.listdir(f"{self.DATA_DIR}/charsets"):
            self.CHARSETS.append(f)
            print(f"Loaded charset file: {f}")

        if not self.CHARSETS:
            print(f"No charset files were found.")

    def load_tilesets(self):
        for f in os.listdir(f"{self.DATA_DIR}/tilesets"):
            self.TILESETS.append(f)
            print(f"Loaded tileset file: {f}")
        
        if not self.TILESETS:
            print(f"No tileset files were found.")

    def load_music(self):
        for f in os.listdir(f"{self.DATA_DIR}/music"):
            self.MUSIC.append(f)
            print(f"Loaded music file: {f}")
        
        if not self.MUSIC:
            print(f"No music files were found.")

    def load_data(self):
        self.load_charsets()
        self.load_tilesets()
        self.load_music()

    def __init__(self, game_name = "Game"):
        self.NAME = game_name

        print(f"Starting OpenRPG Player ({self.NAME})")

        self.load_data()
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        self.SCREEN = pygame.display.set_mode(self.RESOLUTION)
        pygame.display.set_caption(f"OpenRPG Player - {self.NAME}")

        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

        self.IS_RUNNING = True
        self.load_titlescreen()

    def get_font(self, font = "monospace", size = 5):
        pygame.font.init()
        return pygame.font.SysFont(font, size)

    def draw_text(self, font: pygame.font.Font, text = "", color = pygame.Color(255, 255, 255), pos = [100, 100]):
        t_surface = font.render(text, 0, color)
        self.SCREEN.blit(t_surface, t_surface.get_rect(center=self.SCREEN.get_rect().center))

    def load_titlescreen(self):
        self.draw_text(self.get_font(), self.NAME)

    def handle_keystroke(self, e: pygame.event.Event):
        match e.key:
            case pygame.K_SPACE:
                # test audio by pressing space
                if not self.MUSIC:
                    print(f"Can't play music - no file found")
                else:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                    else:
                        pygame.mixer.music.load(f"{self.DATA_DIR}/music/{self.MUSIC[0]}")
                        pygame.mixer.music.play(-1)

    def run(self):
        while self.IS_RUNNING:
            for e in pygame.event.get():
                match e.type:
                    case pygame.QUIT:
                        self.IS_RUNNING = False
                    case pygame.KEYDOWN:
                        self.handle_keystroke(e)
                    case self.REFRESH:
                        pass

        pygame.quit()