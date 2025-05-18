from pydmsd.face.types import FaceDataModel
from pydmsd.ontology import reasoner


def test_face_cardinality_conflict():
    model = FaceDataModel()

    Helicopter = model.create_entity("Helicopter")
    Quadrotor = model.create_entity("Quadrotor")

    # Helicopter has 1 rotor
    Helicopter.create_characteristic(name="rotorSpeed", lower_bound=1, upper_bound=1, value_type=float)

    # Quadrotor has 4 rotors
    Quadrotor.create_characteristic(name="rotorSpeed", lower_bound=4, upper_bound=4, value_type=float)

    assert not reasoner.check_compatibility(Helicopter, Quadrotor)

    print(reasoner.explain_incompatibilities(Helicopter, Quadrotor))
