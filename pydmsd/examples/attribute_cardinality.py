from pydmsd.ontology import types, reasoner

# create the ontology
ontology = types.Ontology()

# define classes
Car = ontology.define_class("Car")
Motorcycle = ontology.define_class("Motorcycle")

# define a shared data property
tire_pressure = ontology.define_data_property("tirePressure", domain=None, range_=[float])

# add conflicting cardinality restrictions
Car.add_exactly_cardinality(tire_pressure, 4)
Motorcycle.add_exactly_cardinality(tire_pressure, 2)

# check compatibility
reasoner.detect_and_explain_incompatibilities(Car, Motorcycle)
