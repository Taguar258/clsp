from clsp.clsp import select

inp = ["/home/clsp/Documents/clsp", "/home/clsp/Documents/clsp/clsp/"] * 40

out = select(inp + list(range(1, 10)) + ([3] * 3), info="Test\nTest2", current=50, rows=60, ignore_warnings=1)

print(out, out.index)
