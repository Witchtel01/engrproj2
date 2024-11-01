import timeit
maxVal = 10


def func():
    for i in range(maxVal):
        for j in range(maxVal):
            for k in range(maxVal):
                for l in range(maxVal):
                    for m in range(maxVal):
                        for n in range(maxVal):
                            print(f"\ri: {i}, j: {j}, k: {k}, l: {l}", end="")
# func()
print("\n"+str(timeit.timeit(stmt="func()", number=1, globals=globals())))
