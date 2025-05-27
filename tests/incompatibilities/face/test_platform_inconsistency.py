from pydmsd.face.types import FaceDataModel
from pydmsd.ontology import reasoner
import owlready2 as owl


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
    RotationsPerMinute = model.create_unit("RotationsPerMinute")
    RotorSpeedRPM = model.create_measurement_system("RotorSpeedRPM", observable=RotorSpeed, unit=RotationsPerMinute)

    Helicopter_A.ontology_class.add_only(rotorSpeed, RotorSpeedRPM.owl_cls)
    Helicopter_B.ontology_class.add_only(rotorSpeed, RotorSpeedRPM.owl_cls)

    assert reasoner.check_compatibility(Helicopter_A, Helicopter_B)

    print(reasoner.explain_incompatibilities(Helicopter_A, Helicopter_B))

    # Platform
    # TODO add to FACE model abstraction. For now, just adding restrictions diretcly to ontology
    with (ontology := model.ontology.owl_ontology):
        ontology.Helicopter_A.is_a.extend([
            owl.Restriction(
                Property=ontology.Helicopter_rotorSpeed,
                type=owl.ONLY,
                value=owl.Restriction(
                    Property=ontology.hasValueType,
                    type=owl.ONLY,
                    value=ontology.FloatValueType
                )
            ),
            owl.Restriction(
                Property=ontology.Helicopter_rotorSpeed,
                type=owl.EXACTLY,
                cardinality=1,
                value=owl.Restriction(
                    Property=ontology.hasValueType,
                    type=owl.EXACTLY,
                    cardinality=1,
                    value=ontology.FloatValueType
                )
            )
        ])
        ontology.Helicopter_A.is_a.extend([
            owl.Restriction(
                Property=ontology.Helicopter_rotorSpeed,
                type=owl.ONLY,
                value=owl.Restriction(
                    Property=ontology.hasValueType,
                    type=owl.ONLY,
                    value=ontology.IntegerValueType
                )
            ),
            owl.Restriction(
                Property=ontology.Helicopter_rotorSpeed,
                type=owl.EXACTLY,
                cardinality=1,
                value=owl.Restriction(
                    Property=ontology.hasValueType,
                    type=owl.EXACTLY,
                    cardinality=1,
                    value=ontology.IntegerValueType
                )
            )
        ])

    assert not reasoner.check_compatibility(Helicopter_A, Helicopter_B)

    print(reasoner.explain_incompatibilities(Helicopter_A, Helicopter_B))
