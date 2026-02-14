from transitions import Machine
from random import randint
import time 

# designed for v2.7
# the generic class (state base class)
State = type("State", (object,), {})

# classes for each state
class LightOn(State):
    def Execute(self):
        print("Light is On")

class LightOff(State):
    def Execute(self):
        print("Light is Off")        


# transitions for the classes 
class Transition(object):
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        print("Transitioning...")

# state machine classes
class SimpleFSM(object):
    def __init__(self, char):
        self.char = char
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.trans = None

    def SetState(self, stateName):
        self.curState = self.states[stateName]

    def Transitions(self, transName):
        self.trans = self.transitions[transName]

    def Execute(self):
        if (self.trans):
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.trans = None
        self.curState.Execute()

# charackter class, attributes, etc.
class Char(object):
    def __init__(self):
        self.FSM = SimpleFSM(self)
        self.LightOn = True

# 
if __name__ == "__main__":
    light = Char()

    light.FSM.states["On"] = LightOn()
    light.FSM.states["Off"] = LightOff()
    light.FSM.transitions["toOn"] = Transition("On")
    light.FSM.transitions["toOff"] = Transition("Off")
    # set the initial state of the FSM
    light.FSM.SetState("On")

    for i in range(20):
        startTime = time.time()
        timeInterval = 1
        while(startTime + timeInterval > time.time()):
            pass
        if(randint(0,2)):
            if (light.LightOn):
                light.FSM.Transitions("toOff")
                light.LightOn = False
            else:
                light.FSM.Transitions("toOn")
                light.LightOn = True 
        light.FSM.Execute()

