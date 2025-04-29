
class LevelManager:
    def __init__(self, game, lotr_bgs):
        self.game = game
        self.current_level = 0
        self.levels = [
            {
                "name": "Helms Deep",
                "background": lotr_bgs[0],
                "good_figure": "Theoden",
                "evil_figure": "Saruman",
                "custom_color": (100, 100, 150),  # Bluish tint
                "custom_message": "Defend the wall of Helms Deep"
            },
            {
                "name": "Minas Tirith",
                "background": lotr_bgs[1],
                "good_figure": "Gandalf",
                "evil_figure": "Witch King",
                "custom_color": (255, 255, 200),  # White/gold tint
                "custom_message": "Protect the White City"
            },
            {
                "name": "Mordor",
                "background": lotr_bgs[2],
                "good_figure": "Aragorn",
                "evil_figure": "Sauron",
                "custom_color": (150, 50, 50),  # Red/dark tint
                "custom_message": "The final battle at the Black Gate"
            }
        ]
    
    def get_current_level(self):
        return self.levels[self.current_level]
    
    def next_level(self):
        self.current_level = (self.current_level + 1) % len(self.levels)
        return self.get_current_level()
    
    def previous_level(self):
        self.current_level = (self.current_level - 1) % len(self.levels)
        return self.get_current_level()
    
    def set_level(self, level_index, game):
        if 0 <= level_index < len(self.levels):
            self.current_level = level_index
        game.reinitialize_ui_elements()
        return self.get_current_level()

