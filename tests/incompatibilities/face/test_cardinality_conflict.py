from pydmsd.face.types import FaceDataModel
from pydmsd.ontology import reasoner


def test_face_cardinality_conflict():
    model = FaceDataModel()

    RotorCraftMessage = model.create_entity("RotorCraftMessage")
    RotorSpeed = model.create_observable("RotorSpeed")
    rotorSpeed = RotorCraftMessage.create_characteristic(
        name="rotorSpeed",
        lower_bound=1,
        upper_bound=None,
        value_type=RotorSpeed
    )

    HelicopterMessage = RotorCraftMessage.create_specialization("HelicopterMessage")
    QuadrotorMessage = RotorCraftMessage.create_specialization("QuadrotorMessage")

    HelicopterMessage.ontology_class.add_exactly_cardinality(rotorSpeed, 1)
    QuadrotorMessage.ontology_class.add_exactly_cardinality(rotorSpeed, 4)

    assert not reasoner.check_compatibility(HelicopterMessage, QuadrotorMessage)
    print(reasoner.explain_incompatibilities(HelicopterMessage, QuadrotorMessage))


