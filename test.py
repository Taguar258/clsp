from clsp.clsp import select

inp = ["/home/clsp/Documents/clsp", "/home/clsp/Documents/clsp/clsp/"] * 4

out = select(list(range(1, 10)), info="Test\nTest2")

print(out)
