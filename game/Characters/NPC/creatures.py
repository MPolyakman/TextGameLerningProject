class Entity:
    def __init__(self, name, max_health: int, position = None):
        self.name = name
        self.current_room = position
        self.inventory = {} # {"name': item}
        self.hp = max_health
        self.max_hp = max_health
        self.alive = True
        self.description = ""
        self.game_log = ''
    
    def __str__(self):
        return getattr(self, "description", "No comments lol")
    
    def repr_stats(self):
        attrs = vars(self)
        for k, v in attrs.items():
            print(f"{k}: {str(v)}")