from pydmsd.face.types import FaceDataModel
from pydmsd.ontology import reasoner


def test_logical_inconsistency():
    model = FaceDataModel()

    # Conceptual
    Helicopter = model.create_entity("Helicopter")
    RotorSpeed = model.create_observable("RotorSpeed")
    rotorSpeed = Helicopter.create_characteristic(name="rotorSpeed", lower_bound=1, upper_bound=1, value_type=RotorSpeed)

    Helicopter_A = Helicopter.create_specialization("Helicopter_A")
    Helicopter_B = Helicopter.create_specialization("Helicopter_B")

    assert reasoner.check_compatibility(Helicopter_A, Helicopter_B)

    print(reasoner.explain_incompatibilities(Helicopter_A, Helicopter_B))

    # Logical
    Hertz = model.create_unit("Hertz")
    RotationsPerMinute = model.create_unit("RotationsPerMinute")
    Hertz.ontology_class.add_disjoint_class(RotationsPerMinute.ontology_class)

    RotorSpeedHertz = model.create_measurement_system("RotorSpeedHertz", observable=RotorSpeed, unit=Hertz)
    RotorSpeedRPM = model.create_measurement_system("RotorSpeedRPM", observable=RotorSpeed, unit=RotationsPerMinute)

    Helicopter_A.ontology_class.add_only(rotorSpeed, RotorSpeedHertz.owl_cls)
    Helicopter_B.ontology_class.add_only(rotorSpeed, RotorSpeedRPM.owl_cls)

    assert not reasoner.check_compatibility(Helicopter_A, Helicopter_B)

    print(reasoner.explain_incompatibilities(Helicopter_A, Helicopter_B))

