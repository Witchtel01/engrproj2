from typing import List

slurryFlowRate = (835200 * 0.00378541) / (24 * 60 * 60)


class Operation:
    def __init__(self, energyConsumption : int, efficiency : float, cost : int):
        self.cons = energyConsumption
        self.efficiency = efficiency
        self.cost = cost

class Pump:
    def __init__(self, efficiency, cost):
        self.efficiency = efficiency
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
    def __init__(self, pipeList : List[Pipe], pumpList : List[Pump], bendList : List[Bend], valveList : List[Valve], cost: int):
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

pumpList = [
    Pump(0.8, 390000),
    Pump(0.83, 460000),
    Pump(0.86, 560000),
    Pump(0.89, 670000),
    Pump(0.92, 808000)
]


def getPurity(fermenter : Operation, distiller : Operation, dehydration : Operation, filter : Operation) -> dict:
    sugarIn = slurryFlowRate * 0.20 * 1599
    fiberIn = slurryFlowRate * 0.20 * 1311
    waterIn = slurryFlowRate * 0.60 * 997
    ethanolIn = 0
    
    
    ethanolOut = 0.51 * sugarIn * fermenter.efficiency
    sugarOut = sugarIn * (1 - fermenter.efficiency)
    waterOut = waterIn
    fiberOut = fiberIn
    co2Waste = 0.49 * sugarIn * fermenter.efficiency
    
    
    waterIn = waterOut
    sugarIn = sugarOut
    fiberIn = fiberOut
    ethanolIn = ethanolOut

    
    fiberOut = fiberIn * (1 - filter.efficiency)
    waterOut = waterIn
    sugarOut = sugarIn
    ethanolOut = ethanolIn
    fiberWaste = fiberIn * filter.efficiency
    
    
    waterIn = waterOut
    sugarIn = sugarOut
    fiberIn = fiberOut
    ethanolIn = ethanolOut
    
    
    waterOut = (waterIn * ethanolIn * ((1 / distiller.efficiency) - 1)) / (waterIn + sugarIn + fiberIn)
    sugarOut = (sugarIn * ethanolIn * ((1/distiller.efficiency) - 1)) / (waterIn + sugarIn + fiberIn)
    fiberOut = (fiberIn * ethanolIn * ((1/distiller.efficiency) - 1)) / (waterIn + sugarIn + fiberIn)
    fiberWaste += fiberIn - fiberOut
    sugarWaste = sugarIn - sugarOut
    waterWaste = waterIn - waterOut


    waterIn = waterOut
    sugarIn = sugarOut
    fiberIn = fiberOut
    ethanolIn = ethanolOut
    
    
    waterOut = waterIn * (1 - dehydration.efficiency)
    ethanolOut = ethanolIn
    sugarOut = sugarIn
    fiberOut = fiberIn
    waterWaste += waterIn * dehydration.efficiency
    
    return {
        "sugarOut" : sugarOut,
        "ethanolOut" : ethanolOut,
        "fiberOut" : fiberOut,
        "waterOut" : waterOut,
        "fiberWaste" : fiberWaste,
        "waterWaste" : waterWaste,
        "sugarWaste" : sugarWaste,
        "CO2Waste" : co2Waste
    }

