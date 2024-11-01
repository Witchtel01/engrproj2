import math
from typing import List

import progressbar

slurryGallonsPerDay = 835200
slurryFlowRate = (slurryGallonsPerDay * 0.00378541) / (24 * 60 * 60)
massFlowRate = slurryFlowRate * (1599 * 0.20 + 0.2 * 1311 + 0.60 * 977)


class Operation:
    def __init__(self, energyConsumption : float, efficiency : float, cost : float):
        self.cons = energyConsumption
        self.efficiency = efficiency
        self.cost = cost

class Pump:
    def __init__(self, quality : int, perfRating : float):
        with open("pumps.txt") as f:
            lines = f.readlines()
            linesplit = [_.split() for _ in lines]
        self.efficiency = [0.8, 0.83, 0.86, 0.89, 0.92][quality]
        self.cost = float(linesplit[int(perfRating / 3 - 2)][quality])
        
class Pipe:
    def __init__(self, quality, diameter, length):
        with open("pipes.txt") as f:
            linesplit = [_.split() for _ in f.readlines()]
        self.frictionFactor = [0.05, 0.03, 0.02, 0.01, 0.005, 0.002][quality]
        self.diameter = diameter
        self.length = length
        self.cost = self.length * float(linesplit[int(diameter * 100 - 10)][quality])

class Bend:
    def __init__(self, lossCoefficient, diameter, cost):
        self.lossCoefficient = lossCoefficient
        self.diameter = diameter
        self.cost = cost

class Valve:
    def __init__(self, quality, diameter):
        with open("valves.txt") as f:
            linesplit = [_.split() for _ in f.readlines()]
        self.flowCoefficient = [800, 700, 600, 500][quality]
        self.diameter = diameter
        self.cost = int(linesplit[int(diameter * 100 - 10)][quality])

class Site:
    def __init__(self, pipeList : List[Pipe], pump : Pump, valve : Valve):
        self.pipeList = pipeList
        self.pump = pump
        self.valve = valve


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


def calculate(
        fermenter : Operation,
        distiller : Operation,
        dehydration : Operation,
        _filter : Operation,
        site : Site
    ) -> dict:
    
    totalEnergyConsumed = 0
    sugarIn = slurryFlowRate * 0.20 * 1599
    fiberIn = slurryFlowRate * 0.20 * 1311
    waterIn = slurryFlowRate * 0.60 * 997
    ethanolIn = 0
    energyIn = kineticEnergyIn(site.pipeList[0])
    totalEnergyConsumed += pumpLoss(site.pump, energyIn)
    totalCost = 0
    
    density = (sugarIn + fiberIn + waterIn + ethanolIn) / ((sugarIn / 1599) + (fiberIn / 1311) + (waterIn / 977) + (ethanolIn / 789))
    flowRate = (sugarIn + fiberIn + waterIn + ethanolIn) / density
    totalCost += site.pump.cost * flowRate
    totalCost += fermenter.cost * flowRate
    
    totalEnergyConsumed += pipeFriction(site.pipeList[0], density, flowRate)
    
    totalEnergyConsumed += valveLoss(site.valve, density, flowRate)
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


    totalEnergyConsumed += valveLoss(site.valve, density, flowRate)
    totalEnergyConsumed += pipeFriction(site.pipeList[1], density, flowRate)
    totalEnergyConsumed += valveLoss(site.valve, density, flowRate)
    totalCost += _filter.cost * flowRate
    
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

    totalEnergyConsumed += valveLoss(site.valve, density, flowRate)
    totalEnergyConsumed += pipeFriction(site.pipeList[2], density, flowRate)
    totalEnergyConsumed += valveLoss(site.valve, density, flowRate)
    totalCost += distiller.cost * flowRate
    
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

    totalEnergyConsumed += valveLoss(site.valve, density, flowRate)
    totalEnergyConsumed += pipeFriction(site.pipeList[3], density, flowRate)
    totalEnergyConsumed += valveLoss(site.valve, density, flowRate)
    totalCost += dehydration.cost * flowRate
    
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
    
    totalEnergyConsumed += valveLoss(site.valve, density, flowRate)
    totalEnergyConsumed += pipeFriction(site.pipeList[4], density, flowRate)
    
    purity = ethanolOut / (waterOut + sugarOut + fiberOut + ethanolOut)
    
    return {
        "sugarOut" : sugarOut,
        "ethanolOut" : ethanolOut,
        "fiberOut" : fiberOut,
        "waterOut" : waterOut,
        "fiberWaste" : fiberWaste,
        "waterWaste" : waterWaste,
        "sugarWaste" : sugarWaste,
        "CO2Waste" : co2Waste,
        "energyConsumed" : totalEnergyConsumed,
        "purity" : purity,
        "totalCost" : totalCost
    }



file = open("piss.txt", "w")
purityFile = open("piss2.txt", "w")

widgets = [' [',
           progressbar.Timer(format='elapsed time: %(elapsed)s'),
           '] ',
           progressbar.Bar("█"),
           " (",
           progressbar.ETA(),
           ") "
]

max = len(fermenterList) * len(distillerList) * len(dehydrationList) * len(filterList) * 6 * 6 * 5 * 4

bar = progressbar.ProgressBar(max_value=max, widgets=widgets).start()


for fermenter in fermenterList:
    for distiller in distillerList:
        for dehydrater in dehydrationList:
            for filt in filterList:
                for pipeQuality in range(6):
                    for universalDiameter in [0.1, 0.11, 0.12, 0.13, 0.14, 0.15]:
                        for pumpQuality in range(5):
                            for valveQuality in range(4):
                                site = Site(
                                    [Pipe(pipeQuality, universalDiameter, _) for _ in [10.78, 1.53, 8.62, 1.53, 3.05]],
                                    Pump(pumpQuality, 27),
                                    Valve(2, universalDiameter)
                                )
                                calc = calculate(fermenter, distiller, dehydrater, filt, site)
                                file.write(str(calc)+"\n\n")
                                purityFile.write(str(calc.get("purity"))+"\n\n")
                                bar.next()

file.close()
purityFile.close()