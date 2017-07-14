from tkinter import *
from math import *
from time import sleep

class LSystem:    
    def __init__(self):
        self.variables = ["F", "G"]
        self.constants = ["+", "-", "[", "]"]
        self.axiom = "F-G-G"
        self.rules = [["F", "F-G+F+G-F"], ["G", "GG"]]
        self.string = ""
        self.actions = [["F", "draw", "5"], ["G", "draw", "5"], ["-", "rotateright", "120"], ["+", "rotateleft", "120"], ["[", "savepos"], ["[", "saveangle"], ["]", "getpos"], ["]", "getangle"]]
        self.positions = []
        self.angles = []
        self.n = 0
        self.t = Tk()
        self.t.resizable(False, False)
        self.c = Canvas(self.t, width=1280, height=1024, bg="#FFFFFF")
        self.c.bind("<Button-1>", self.step_forward)
        self.c.bind("<Button-3>", self.step_back)
        self.c.pack()
        self.run()
        
    def step_back(self, event):
        if self.n == 1:
            return
        self.n -= 1
        string = self.axiom
        tempstring = ""
        for i in range(self.n):
            tempstring = ""
            for j in range(len(string)):
                part = string[j:j+1]
                templen = len(tempstring)
                for rule in self.rules:
                    if rule[0] == part:
                        tempstring += rule[1]
                if templen == len(tempstring):
                    tempstring += part
            string = tempstring
        self.string = string
        print(self.string)
        self.c.delete("all")
        self.t.title("L-System    n: " + str(self.n - 1))
        self.draw()
        
    def step_forward(self, event):
        self.n += 1
        string = self.axiom
        tempstring = ""
        for i in range(self.n):
            tempstring = ""
            for j in range(len(string)):
                part = string[j:j+1]
                templen = len(tempstring)
                for rule in self.rules:
                    if rule[0] == part:
                        tempstring += rule[1]
                if templen == len(tempstring):
                    tempstring += part
            string = tempstring
        self.string = string
        print(self.string)
        self.c.delete("all")
        self.t.title("L-System    n: " + str(self.n - 1))
        self.draw()
        
    def run(self):
        self.step_forward(None)
        while True:
            self.c.update()
            self.t.update()

    def draw(self):
        self.angle = 0
        self.x = 100
        self.y = 924
        for i in range(len(self.string)):
            self.c.update()
            self.t.update()
            sleep(0.001)
            part = self.string[i:i+1]
            for action in self.actions:
                if action[0] == part:
                    if action[1] == "draw":
                        x2 = (int(action[2]) * cos(radians(self.angle))) + self.x
                        y2 = (int(action[2]) * sin(radians(self.angle))) + self.y
                        self.c.create_line(self.x, self.y, x2, y2, fill="#000000")
                        self.x = x2
                        self.y = y2
                    elif action[1] == "move":
                        x2 = (int(action[2]) * cos(radians(self.angle))) + self.x
                        y2 = (int(action[2]) * sin(radians(self.angle))) + self.y
                        self.x = x2
                        self.y = y2
                    elif action[1] == "rotateright":
                        if self.angle >= int(action[2]):
                            self.angle -= int(action[2])
                        else:
                            self.angle = 360 - int(action[2]) + self.angle
                    elif action[1] == "rotateleft":
                        self.angle = int(self.angle + int(action[2])) % 360
                    elif action[1] == "savepos":
                        self.positions.append([self.x, self.y])
                    elif action[1] == "getpos":
                        position = self.positions[-1]
                        self.x = position[0]
                        self.y = position[1]
                        del self.positions[-1]
                    elif action[1] == "saveangle":
                        self.angles.append(self.angle)
                    elif action[1] == "getangle":
                        angle = self.angles[-1]
                        del self.angles[-1]
                        self.angle = angle
                        
if __name__ == "__main__":
    LS = LSystem()
