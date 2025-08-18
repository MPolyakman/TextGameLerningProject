from events import Event, GiveItemEvent, TakeItemEvent, PutItemEvent

class Entity:
    def __init__(self, name,  position = None, max_health = 100):
        self.name = name
        self.current_room = position
        self.inventory = {} # {"name': item}
        self.hp = max_health
        self.max_hp = max_health
        self.alive = True
        self.description = ""
        self.game_log = ''

    def give(self, item, target) -> Event:
        event = GiveItemEvent(self, item, target)
        return event
    
    def take(self, item_name):
        if self.current_room != None and item_name in self.current_room.items.keys():
            return TakeItemEvent(self, item_name, self.current_room)
        
    def put(self, item_name):
        if self.current_room != None and item_name in self.inventory.keys():
            return PutItemEvent(self, item_name, self.current_room)
    
    def __str__(self):
        return getattr(self, "description", "No comments lol")
    
    def repr_stats(self):
        attrs = vars(self)
        for k, v in attrs.items():
            print(f"{k}: {str(v)}")