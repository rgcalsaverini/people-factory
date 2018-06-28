from sample_config import asian, european, african
import random


for i in range(1):
    # if random.uniform(0, 1) < 0.5:
    person = european.random()
    # elif random.uniform(0, 1) < 0.75:
    #     person = african.random()
    # else:
    #     person = asian.random()

    # person = asian.random()
    person.make_portrait()
    person.export_svg('./out/%d.svg' % i)
