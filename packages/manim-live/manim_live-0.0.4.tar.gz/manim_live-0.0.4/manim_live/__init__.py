import pyglet
from pyglet import shapes
import os
import sys

class ManimLive:
    def __init__(self, directory, fullscreen=False):
        self.directory = directory
        self.window = pyglet.window.Window(fullscreen=fullscreen)
        self.files = {}
        for i, filename in enumerate(os.listdir(self.directory)):
            if filename.endswith(".mp4"):
                self.files[filename[:-4]] = {}
                self.files[filename[:-4]]['name'] = filename
                self.files[filename[:-4]]['number'] = i
            else:
                continue
        self.menu_el_rows = 4
        self.menu_el_cols = 3

    def run(self):
        pyglet.app.run()

    def list_files(self):
        for i in self.files:
            print(f"file name: {self.files[i]['name']} order number: {self.files[i]['number']}")
            
    def change_order(self, file_numbers):
        for i, f in enumerate(self.files):
            self.files[f]['number'] = file_numbers[i]

    def play_anim(self):
        player = pyglet.media.Player()

        for i in range(len(self.files)):
            for f in self.files: 
                if self.files[f]['number'] == i:
                    MediaLoad = pyglet.media.load(os.path.join(self.directory, self.files[f]['name']))
                    player.queue(MediaLoad)
            
        player.play()

        @self.window.event
        def on_draw():
            if player.source and player.source.video_format:
                player.get_texture().blit(0,0)   

        def on_eos():
            player.pause()

        @self.window.event
        def on_key_press(key, modifiers):
            if key == pyglet.window.key.N and not player.playing:
                player.play()

        player.push_handlers(on_eos) 

    def menu(self):
        menu_rect = []

        for i in range(self.menu_el_rows):
            for j in range(self.menu_el_cols):
                menu_rect.append(self.menu_el(j * self.window.width/self.menu_el_cols, i * self.window.height/self.menu_el_rows))

        @self.window.event
        def on_draw():
            self.window.clear()
            for i in menu_rect:
                i.draw()
            
    def menu_el(self, x, y):
        return shapes.Rectangle(x + self.window.height*0.1/4, y + self.window.height*0.1/4, self.window.width/self.menu_el_cols - self.window.height*0.1/2, self.window.height/self.menu_el_rows - self.window.height*0.1/2, color=(55, 55, 255))
            