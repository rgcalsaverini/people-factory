from sample_config import asian, european, african
import random

if random.uniform(0, 1) < 0.5:
    person = european.random()
elif random.uniform(0, 1) < 0.75:
    person = african.random()
else:
    person = asian.random()

# person = african.random()
person.make_portrait()
person.export_svg('out.svg')
