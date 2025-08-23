from events import LeaveInteractionEvent

class Interaction:
    def __init__(self, player, chars: list):
        self.player = player
        self.chars = chars
        self.room = player.current_room
        self.dialog_log = {}
        for c in chars:
            self.dialog_log[c] = ''
    
    def join(self, char):
        if char in self.chars or char.current_room is not self.room:
            return False
        self.chars.append(char)
        self.dialog_log[char] = ''
        return True
    
    def dialog_log_upd(self, char, words):
        try:
            self.dialog_log[char] += words + '\n'
        except:
            self.dialog_log[char] = words + '\n'
    
    def leave(self, char_name):
        for c in self.chars:
            if c.name == char_name:
                self.chars.remove(c)
                return True
        else:
            return False
