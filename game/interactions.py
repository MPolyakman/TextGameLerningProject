from events import LeaveInteractionEvent

class Interaction:
    def __init__(self, chars: list):
        self.chars = chars
        self.dialog_log = {}
        for c in chars:
            self.dialog_log[c] = ''
    
    def join(self, char):
        if char in self.chars:
            return False
        self.chars.append(char)
        self.dialog_log[char] = ''
        return True
    
    def dialog_log_upd(self, char, words):
        self.dialog_log[char] += words + '\n'
    
    def leave(self, char):
        if char in self.chars:
            self.chars.remove(char)
            return LeaveInteractionEvent(char)
