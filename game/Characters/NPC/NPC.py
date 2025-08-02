from creatures import Creature
import ollama


class NPC(Creature):
    def __init__(self, name, position, max_health, biography):
        super().__init__(name, position, max_health)
        self.biography = biography
        self.history = ''

    def say(self, messages):
        messages.append({'role': 'system', 'content': self.biography})
        messages.append({'role': 'user', 'content': self.history})
        btw = ollama.chat(model='llama3:instruct', messages=messages)
        ans = btw['message']['content']
        messages.append({'role': 'system', 'content': ans})
        messages.append({'role': 'user', 'content': "Вкратце перескажи всё то что, говорил этот NPC и всё что с ним происходило за исключением исходного описания"})
        self.history = ollama.chat(model='llama3:instruct', messages=messages)['message']['content']
        return ans


    
