from pydmsd.ontology import types, reasoner

# create the DMSD model
model = types.Ontology()

# define message classes
CarMessage = model.define_class("CarMessage")
MotorcycleMessage = model.define_class("MotorcycleMessage")

# define an observable
Pressure = model.define_observable("Pressure")

# define a shared message attribute
tire_pressure = model.define_object_property("tirePressure", domain=None, range_=Pressure)

# add cardinalities
CarMessage.add_exactly_cardinality(tire_pressure, 4)
MotorcycleMessage.add_exactly_cardinality(tire_pressure, 2)

# check compatibility
assert not reasoner.check_compatibility(CarMessage, MotorcycleMessage)
print(reasoner.explain_incompatibilities(CarMessage, MotorcycleMessage))


