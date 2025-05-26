from pydmsd.face.types import FaceDataModel
from pydmsd.ontology import reasoner


def test_face_cardinality_conflict():
    model = FaceDataModel()

    RotorCraft = model.create_entity("RotorCraft")
    RotorSpeed = model.create_observable("RotorSpeed")
    rotorSpeed = RotorCraft.create_characteristic(name="rotorSpeed", lower_bound=1, upper_bound=None, value_type=RotorSpeed)

    Helicopter = RotorCraft.create_specialization("Helicopter")
    Quadrotor = RotorCraft.create_specialization("Quadrotor")

    Helicopter.ontology_class.add_exactly_cardinality(rotorSpeed, 1)
    Quadrotor.ontology_class.add_exactly_cardinality(rotorSpeed, 4)

    assert not reasoner.check_compatibility(Helicopter, Quadrotor)

    print(reasoner.explain_incompatibilities(Helicopter, Quadrotor))
