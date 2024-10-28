from typing import List
class Operation:
    def __init__(self, energyConsumption : int, efficiency : float, cost : int):
        self.cons = energyConsumption
        self.efficiency = efficiency
        self.cost = cost

class Pump:
    def __init__(self, efficiency, height, cost):
        self.efficiency = efficiency
        self.height = height
        self.cost = cost
        
class Pipe:
    def __init__(self, frictionFactor, diameter, cost, _type = "liquid"):
        self.frictionFactor = frictionFactor
        self.diameter = diameter
        self.cost = cost
        self.type = _type

class Bend:
    def __init__(self, lossCoefficient, diameter, cost):
        self.lossCoefficient = lossCoefficient
        self.diameter = diameter
        self.cost = cost

class Valve:
    def __init__(self, flowCoefficient, diameter, cost):
        self.flowCoefficient = flowCoefficient
        self.diameter = diameter
        self.cost = cost

class Site:
    def __init__(self, pipeList : List[Pipe], pumpList : List[Pump], bendList : List[Bend], valveList : List[Valve]):
        pass


fermenterList = [
    Operation(46600, 0.5, 320000),
    Operation(47200, 0.75, 380000),
    Operation(47500, 0.9, 460000),
    Operation(48000, 0.95, 1100000)
]

distillerList = [
    Operation(47004, 0.81, 390000),
    Operation(47812, 0.9, 460000),
    Operation(48200, 0.915, 560000),
    Operation(49500, 0.98, 1370000)
]

dehydrationList = [
    Operation(48800, 0.5, 200000),
    Operation(49536, 0.75, 240000),
    Operation(50350, 0.9, 280000),
    Operation(51000, 0.98, 480000)
]

filterList = [
    Operation(48800, 0.5, 200000),
    Operation(49536, 0.75, 240000),
    Operation(50350, 0.9, 280000),
    Operation(51000, 0.98, 480000)
]
