from pathlib import Path
from mididings.engine import scenes, current_scene, current_subscene
from extensions.common import (
    Terminal
)
class PlaylistManager:
    def __init__(self):
        self.playlist = Playlist()
        self.has_subscene = None

    def __call__(self, ev):
        scene = self.get_scene_name()
        self.has_subscene = scenes()[current_scene()][1]
        subscene = self.get_subscene_name()
        path = f"{scene}/{subscene}" if subscene else scene
        self.playlist.create(f"/media/soundlib/{path}")
        self.playlist.listing()

    def get_scene_name(self):
        return scenes()[current_scene()][0]

    def get_subscene_name(self):
        return (
            scenes()[current_scene()][1][current_subscene() - 1]
            if self.has_subscene
            else None
        )

class Playlist:
    def __init__(self):
        self.songs = []
        self.terminal = Terminal()

    def create(self, path):
        self.songs = [
            p.resolve()
            for p in sorted(Path(path).glob("**/*"))
            if p.suffix.lower() in {".mp3"}
        ]
  
    def len(self):
        return len(self.songs)

    def listing(self):
        if not self.songs:
            self.terminal.write_line("No files found in " + path)
            return

        rank = 0
        for song in self.songs:
            rank += 1
            self.terminal.write_line2(str(rank).zfill(2), song)
