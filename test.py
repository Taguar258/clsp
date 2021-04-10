import pycountry
from clsp import select

inp = [c.alpha_2 for c in pycountry.countries]

out = select(inp, info="Select your Country:", rows=10)

print("You selected: " + out.value)
