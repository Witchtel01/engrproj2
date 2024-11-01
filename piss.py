import math
from typing import List

slurryFlowRate = (835200 * 0.00378541) / (24 * 60 * 60)
massFlowRate = slurryFlowRate * (1599 * 0.20 + 0.2 * 1311 + 0.60 * 977)


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
    def __init__(self, frictionFactor, diameter, cost, length, _type = "liquid"):
        self.frictionFactor = frictionFactor
        self.diameter = diameter
        self.cost = cost
        self.length = length
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
        self.pipeList = pipeList
        self.pumpList = pumpList
        self.bendList = bendList
        self.valveList = valveList
        self.cost = cost


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

def electricalEnergyIn(fermenter : Operation, distiller : Operation, dehydration : Operation, _filter : Operation, pump : Operation) -> float:
    return sum(fermenter.cons, distiller.cons, dehydration.cons, _filter.cons, pump.cons)

def kineticEnergyIn(pipe : Pipe):
    # KE = 1/2mv^2
    return 0.5 * massFlowRate * ((slurryFlowRate / (((pipe.diameter / 2) ** 2) * math.pi)) ** 2)

def pumpLoss(pump : Operation, eIn : float):
    return (1 - pump.efficiency) * eIn

def pipeFriction(pipe : Pipe, density : float, flowRate : float):
    hdw = pipe.frictionFactor * (8 / (9.80 * math.pi ** 2)) * ((pipe.length * flowRate ** 2) / (pipe.diameter ** 5))
    return density * flowRate * hdw

def bendLoss():
    return 0

def valveLoss(valve : Valve, density : float, flowRate : float):
    hdw = valve.flowCoefficient * (flowRate / (math.pi * (valve.diameter / 2) ** 2) ** 2) / (2 * 9.80)
    return density * flowRate * hdw


def calculate(fermenter : Operation, distiller : Operation, dehydration : Operation, _filter : Operation, site : Site) -> dict:
    totalEnergyConsumed = 0
    sugarIn = slurryFlowRate * 0.20 * 1599
    fiberIn = slurryFlowRate * 0.20 * 1311
    waterIn = slurryFlowRate * 0.60 * 997
    ethanolIn = 0
    energyIn = kineticEnergyIn(site.pipeList[0])
    totalEnergyConsumed += pumpLoss(site.pumpList[0], energyIn)
    
    density = (sugarIn + fiberIn + waterIn + ethanolIn) / ((sugarIn / 1599) + (fiberIn / 1311) + (waterIn / 977) + (ethanolIn / 789))
    flowRate = (sugarIn + fiberIn + waterIn + ethanolIn) / density
    
    totalEnergyConsumed += pipeFriction(site.pipeList[0], density, flowRate)
    
    totalEnergyConsumed += valveLoss(site.valveList[0], density, flowRate)
    ethanolOut = 0.51 * sugarIn * fermenter.efficiency
    sugarOut = sugarIn * (1 - fermenter.efficiency)
    waterOut = waterIn
    fiberOut = fiberIn
    co2Waste = 0.49 * sugarIn * fermenter.efficiency
    
    
    waterIn = waterOut
    sugarIn = sugarOut
    fiberIn = fiberOut
    ethanolIn = ethanolOut
    
    
    
    
    
    
    density = (sugarIn + fiberIn + waterIn + ethanolIn) / ((sugarIn / 1599) + (fiberIn / 1311) + (waterIn / 977) + (ethanolIn / 789))
    flowRate = (sugarIn + fiberIn + waterIn + ethanolIn) / density

    totalEnergyConsumed += valveLoss(site.valveList[1], density, flowRate)
    totalEnergyConsumed += pipeFriction(site.pipeList[1], density, flowRate)
    totalEnergyConsumed += valveLoss(site.valveList[2], density, flowRate)

    
    fiberOut = fiberIn * (1 - _filter.efficiency)
    waterOut = waterIn
    sugarOut = sugarIn
    ethanolOut = ethanolIn
    fiberWaste = fiberIn * _filter.efficiency
    
    
    waterIn = waterOut
    sugarIn = sugarOut
    fiberIn = fiberOut
    ethanolIn = ethanolOut
    
    
    
    density = (sugarIn + fiberIn + waterIn + ethanolIn) / ((sugarIn / 1599) + (fiberIn / 1311) + (waterIn / 977) + (ethanolIn / 789))
    flowRate = (sugarIn + fiberIn + waterIn + ethanolIn) / density

    totalEnergyConsumed += valveLoss(site.valveList[3], density, flowRate)
    totalEnergyConsumed += pipeFriction(site.pipeList[2], density, flowRate)
    totalEnergyConsumed += valveLoss(site.valveList[4], density, flowRate)
    
    
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
    
    density = (sugarIn + fiberIn + waterIn + ethanolIn) / ((sugarIn / 1599) + (fiberIn / 1311) + (waterIn / 977) + (ethanolIn / 789))
    flowRate = (sugarIn + fiberIn + waterIn + ethanolIn) / density

    totalEnergyConsumed += valveLoss(site.valveList[5], density, flowRate)
    totalEnergyConsumed += pipeFriction(site.pipeList[3], density, flowRate)
    totalEnergyConsumed += valveLoss(site.valveList[6], density, flowRate)
    
    waterOut = waterIn * (1 - dehydration.efficiency)
    ethanolOut = ethanolIn
    sugarOut = sugarIn
    fiberOut = fiberIn
    waterWaste += waterIn * dehydration.efficiency
    
    
    
    waterIn = waterOut
    sugarIn = sugarOut
    fiberIn = fiberOut
    ethanolIn = ethanolOut

    density = (sugarIn + fiberIn + waterIn + ethanolIn) / ((sugarIn / 1599) + (fiberIn / 1311) + (waterIn / 977) + (ethanolIn / 789))
    flowRate = (sugarIn + fiberIn + waterIn + ethanolIn) / density
    
    totalEnergyConsumed += valveLoss(site.valveList[7], density, flowRate)
    totalEnergyConsumed += pipeFriction(site.pipeList[4], density, flowRate)
    
    
    return {
        "sugarOut" : sugarOut,
        "ethanolOut" : ethanolOut,
        "fiberOut" : fiberOut,
        "waterOut" : waterOut,
        "fiberWaste" : fiberWaste,
        "waterWaste" : waterWaste,
        "sugarWaste" : sugarWaste,
        "CO2Waste" : co2Waste,
        "energyConsumed" : totalEnergyConsumed
    }
