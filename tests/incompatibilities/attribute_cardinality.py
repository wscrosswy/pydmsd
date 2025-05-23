from pydmsd.ontology import types, reasoner


def test_attribute_cardinality():
    # create the ontology
    ontology = types.Ontology()

    # define classes
    Car = ontology.define_class("Car")
    Motorcycle = ontology.define_class("Motorcycle")

    Pressure = ontology.define_class("Pressure")

    # define a shared property
    tire_pressure = ontology.define_object_property("tirePressure", domain=None, range_=Pressure)

    # add conflicting cardinality restrictions
    Car.add_exactly_cardinality(tire_pressure, 4)
    Motorcycle.add_exactly_cardinality(tire_pressure, 2)

    # check compatibility
    assert not reasoner.check_compatibility(Car, Motorcycle)
    print(reasoner.explain_incompatibilities(Car, Motorcycle))

if __name__ == "__main__":
    test_attribute_cardinality()