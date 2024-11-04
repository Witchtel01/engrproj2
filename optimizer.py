with open("data.txt") as f:
    data = [eval(_.strip()) for _ in f.readlines() 
            if not _.strip() == ""]




# Normalize the cost and energy consumed using precalculated
# mins and maxes
def normalizeEnergy(x : float) -> float:
    return (x - 612142) / (3486279 - 612142) * 10
def normalizeCost(x : float) -> float:
    return(x - 47683) / (133314 - 47683) * 10
normalized = [normalizeEnergy(_.get("energyConsumed"))
              + normalizeCost(_.get("totalCost")) for _ in data]


# Search through the data to find the minimum normalized value
minNormal = 1000
index = 0
for i in range(len(data)):
    if data[i].get("purity") < 0.98:
        continue
    if normalized[i] < minNormal:
        index = i
        minNormal = normalized[i]
print(data[index])

def get_loop_values(index):
    """Given an index, returns the indicies of the nested loop

    Args:
        index (int): The index to back calculate

    Returns:
        list[int]: List of indices for each loop
    """    
    
    # Lengths of each nested loop
    lengths = [4, 4, 4, 4, 6, 6, 5, 4]
    # List to store products
    cumuProducts = [1] * len(lengths)
    # Loop through and calculate the blocks to int division by
    for i in range(len(lengths) - 2, -1, -1):
        cumuProducts[i] = cumuProducts[i + 1] * lengths[i + 1]
    
    loop_values = [0] * len(lengths)
    
    # Calculates the indicies, stores to loop_values
    for i in range(len(lengths)):
        loop_values[i] = index // cumuProducts[i]
        index %= cumuProducts[i]
    
    return loop_values

# print index
l = get_loop_values(index)
print(l)




# # This is optional to test if it is actually the same:



# from main import (Pipe, Pump, Site, Valve, calculate,
#                   dehydrationList, distillerList,
#                   fermenterList, filterList)

# pipeQuality = range(6)
# universalDiameter = [0.1, 0.11, 0.12, 0.13, 0.14, 0.15]
# pumpQuality = range(5)
# valveQuality = range(4)
# site = Site(
#     [Pipe(pipeQuality[5], universalDiameter[5], _)\
    # for _ in [10.78, 1.53, 8.62, 1.53, 3.05]],
#     Pump(pumpQuality[0], 27),
#     Valve(2, universalDiameter[5])
# )
# print(calculate(fermenterList[1], distillerList[1],\
    # dehydrationList[3], filterList[2], site))




# Print Formatted Output
print(f"Fermenter {l[0]+1}")
print(f"Distiller {l[1]+1}")
print(f"Dehydrater {l[2]+1}")
print(f"Filter {l[3]+1}")
print(f"Pipe Quality {l[4]+1}")
print(f"Diameter {l[5]+1}")
print(f"Pump Quality {l[6]+1}")
print(f"Valve Quality {l[7]+1}")

# Simple calculations:
print(f"Ethanol per day: "+\
    f"{data[index].get("ethanolOut")*86400}")
print(f"Energy per day: "+\
    f"{data[index].get("ethanolOut")*21160177.2}")
print(f"Energy ROI: {21160177.2*data[index
        ].get("ethanolOut")/data[index
        ].get("energyConsumed")}")
