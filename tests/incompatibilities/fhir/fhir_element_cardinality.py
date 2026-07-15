from pydmsd.fhir.fhir_types import FhirDataModel, Datatype
from pydmsd.ontology import reasoner

def test_fhir_element_cardinality():
    model = FhirDataModel()

    # define observables (will be disjoint)
    Pressure = model.create_datatype("Pressure")
    Speed = model.create_datatype("Speed")

    # define base Vehicle resource - has 0..* tire pressures
    VehicleResource = model.create_resource("VehicleResource")
    VehicleResource.create_element("tirePressure", 0, None, Pressure)

    # define car profile
    CarProfile = model.create_resource("CarProfile")
    CarProfile.ontology_class.owl_cls.is_a.append(VehicleResource.ontology_class.owl_cls)
    CarProfile.create_element("tirePressure", 4, 4, Pressure)

    # define motorcycle profile
    MotorcycleProfle = model.create_resource("MotorcycleProfle")
    MotorcycleProfle.ontology_class.owl_cls.is_a.append(VehicleResource.ontology_class.owl_cls)
    MotorcycleProfle.create_element("tirePressure", 2, 2, Pressure)

    # check compatibility
    assert not reasoner.check_compatibility(CarProfile, MotorcycleProfle)
    print(reasoner.explain_incompatibilities(CarProfile, MotorcycleProfle))

if __name__ == "__main__":
    test_fhir_element_cardinality()
