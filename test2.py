with open("piss.txt") as f:
    data = [eval(_.strip()) for _ in f.readlines() if not _.strip() == ""]
