with open("piss.txt") as f:
    data = [eval(_.strip()) for _ in f.readlines() if not _.strip() == ""]

print(len(data))

# removers = []
# for i in range(len(data)):
#     if data[i].get("purity") < 0.98:
#         removers.append(i)

# data = [_ for _ in data if not data.index(_) in removers]

# print(len(data))
def normalizeEnergy(x : float) -> float:
    return (x - 612142) / (3486279 - 612142) * 10
def normalizeCost(x : float) -> float:
    return(x - 47683) / (133314 - 47683) * 10
normalized = [normalizeEnergy(_.get("energyConsumed")) + normalizeCost(_.get("totalCost")) for _ in data]


minNormal = 1000
index = 0
for i in range(len(data)):
    if data[i].get("purity") < 0.98:
        continue
    if normalized[i] < minNormal:
        index = i
        minNormal = normalized[i]
print(data[index])
print(index)

def get_loop_values(index):
    lengths = [4, 4, 4, 4, 6, 6, 5, 4]
    cumuProducts = [1] * len(lengths)
    for i in range(len(lengths) - 2, -1, -1):
        cumuProducts[i] = cumuProducts[i + 1] * lengths[i + 1]
    
    loop_values = [0] * len(lengths)
    
    for i in range(len(lengths)):
        loop_values[i] = index // cumuProducts[i]
        index %= cumuProducts[i]
    
    return loop_values
print(get_loop_values(index))

from piss import (Pipe, Pump, Site, Valve, calculate,
                  dehydrationList, distillerList, fermenterList, filterList)

pipeQuality = range(6)
universalDiameter = [0.1, 0.11, 0.12, 0.13, 0.14, 0.15]
pumpQuality = range(5)
valveQuality = range(4)
site = Site(
    [Pipe(pipeQuality[5], universalDiameter[5], _) for _ in [10.78, 1.53, 8.62, 1.53, 3.05]],
    Pump(pumpQuality[0], 27),
    Valve(2, universalDiameter[5])
)
print(calculate(fermenterList[1], distillerList[1], dehydrationList[3], filterList[2], site))