from person_gen.generator import Generator

generator = Generator.from_file('config.json')
person = generator.random_person()
person.make_portrait()
person.export_portrait('out.svg')
