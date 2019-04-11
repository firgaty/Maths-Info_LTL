class StateMachine:
    def __init__(self):
        self.handlers = {} # dictionnaire
        self.startState = None
        self.endStates = [] # list

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, txt):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError(" .set_start() doit être devant .run()")
        if not self.endStates:
            raise  InitializationError(" end_state ne peut pas être vide")
    
        while True:
            (newState, txt) = handler(txt)
            if newState.upper() in self.endStates:
                print("Arrêt de la machine : ", newState)
                break 
            else:
                handler = self.handlers[newState.upper()]    
