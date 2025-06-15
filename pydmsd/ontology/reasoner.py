import attrs
import owlready2 as owl
import typing as ty

import pydmsd.face.types as face
import pydmsd.fhir.fhir_types as fhir
from .types import Cardinality, Ontology, OntologyClass


def run_reasoner(ontology: Ontology):
    """Run the HermiT reasoner on the given ontology."""
    print("Running reasoner...")
    with ontology.owl_ontology:
        owl.sync_reasoner()


def _unwrap_ontology_class(obj):
    if isinstance(obj, face.Entity) or isinstance(obj, fhir.Resource):
        return obj.ontology_class
    elif isinstance(obj, OntologyClass):
        return obj
    else:
        raise TypeError(f"Unsupported input: {obj}")


def _get_closed_world_intersection(class1, class2):
    """
    Create and return an intersection of `class1` an `class2` with "max cardinality 0" property restrictions
    for all properties in the symmetric difference of the two classes' sets of properties.

    Under OWL semantics, omission does not imply negation. If one class A has a required property,
    but class B does not require that property, they are not disjoint under OWL semantics.
    This is the "open world assumption" - if something is not stated, that doesn't mean it's not true.
    For our purposes, we would like to infer that message A is not compatible with message B if message B
    does not have all the required properties of message B. For that to be true, we must operate under
    a "closed world assumption". That is not part of OWL semantics, but we can emulate it by (temporarily)
    adding explicit restrictions that properties in A but not in B have a max cardinality of 0 in B and vice-versa.
    Specifically, let the set of properties in A be P_A and the set of properties in B be P_B.
    We temporarily add (P_A - P_B) properties to B  and (P_B - P_A) properties to A, all with
    max cardinality = 0 restrictions.
    """
    cwi = class1.ontology.define_class(name=f"cwi_{class1.name}_{class2.name}")
    cwi.add_superclass(class1)
    cwi.add_superclass(class2)

    required1 = class1.required_properties
    required2 = class2.required_properties
    declared1 = class1.declared_properties
    declared2 = class2.declared_properties

    missing_from_2 = set(required1) - declared2
    missing_from_1 = set(required2) - declared1

    for prop in missing_from_1.union(missing_from_2):
        cwi.add_max_cardinality(prop, 0)

    for prop in missing_from_1:
        cwi.add_max_cardinality(prop, 0)

    return cwi


def check_compatibility(class1, class2) -> bool:
    # TODO use singledispatch
    class1 = _unwrap_ontology_class(class1)
    class2 = _unwrap_ontology_class(class2)
    ontology = class1.ontology

    test_class = _get_closed_world_intersection(class1, class2)

    run_reasoner(ontology)

    is_compatible = owl.Nothing not in test_class.owl_cls.equivalent_to

    ontology.destroy(test_class)

    return is_compatible


def _explain_explicit_disjointness(class1, class2):
    """Detect explicit disjoint axioms between class1 and class2."""
    explicit_disjoint_axioms = []

    if hasattr(class1.owl_cls, "disjoint_with") and class2.owl_cls in class1.owl_cls.disjoint_with:
        explicit_disjoint_axioms.append(
            f"{class1.name} is explicitly declared disjoint with {class2.name}."
        )
    if hasattr(class2.owl_cls, "disjoint_with") and class1.owl_cls in class2.owl_cls.disjoint_with:
        explicit_disjoint_axioms.append(
            f"{class2.name} is explicitly declared disjoint with {class1.name}."
        )

    return explicit_disjoint_axioms


def _explain_property_presence_conflicts(class1, class2):
    """Detect required properties in one class missing from the other."""
    missing = []
    missing_from_2 = class1.required_properties - class2.declared_properties
    for prop in missing_from_2:
        missing.append(
            f"{class1.name} requires property '{prop.name}' which is missing in {class2.name}."
        )
    missing_from_1 = class2.required_properties - class1.declared_properties
    for prop in missing_from_1:
        missing.append(
            f"{class2.name} requires property '{prop.name}' which is missing in {class1.name}."
        )
    return missing


def _cardinalities_overlap(card1: Cardinality, card2: Cardinality) -> bool:
    return not (
        (card1.max is not None and card1.max < card2.min) or
        (card2.max is not None and card2.max < card1.min)
    )


def _explain_cardinality_conflicts(class1, class2):
    """Detect min > max contradictions between two OntologyClasses on shared properties."""
    cardinality_conflicts = []

    for prop in class1.declared_properties & class2.declared_properties:
        card1 = class1.cardinalities.get(prop, Cardinality(None, None))
        card2 = class2.cardinalities.get(prop, Cardinality(None, None))

        if card2.max is not None and card1.min > card2.max:
            cardinality_conflicts.append(
                f"Property {prop.name} has conflicting cardinality restrictions: "
                f"{class1.name} requires min {card1.min}, but {class2.name} requires max {card2.max}."
            )
        if card2.min is not None and card1.max is not None and card2.min > card1.max:
            cardinality_conflicts.append(
                f"Property {prop.name} has conflicting cardinality restrictions: "
                f"{class2.name} requires min {card2.min}, but {class1.name} requires max {card1.max}."
            )

    return cardinality_conflicts


@attrs.define
class IncompatibilityExplanation:
    explicit_disjoint_axioms: ty.List[str]
    cardinality_conflicts: ty.List[str]
    property_presence_conflicts: ty.List[str]

    def __str__(self):
        parts = ["Classes are disjoint due to:"]
        if self.explicit_disjoint_axioms:
            parts.append("  Explicit Disjointness Axioms:")
            for reason in self.explicit_disjoint_axioms:
                parts.append(f"    - {reason}")
        if self.cardinality_conflicts:
            parts.append("  Cardinality Conflicts:")
            for reason in self.cardinality_conflicts:
                parts.append(f"    - {reason}")
        if self.property_presence_conflicts:
            parts.append("  Missing Required Properties:")
            for reason in self.property_presence_conflicts:
                parts.append(f"    - {reason}")

        return "\n".join(parts)


def explain_incompatibilities(class1, class2) -> IncompatibilityExplanation:
    # TODO use singledispatch
    class1 = _unwrap_ontology_class(class1)
    class2 = _unwrap_ontology_class(class2)

    return IncompatibilityExplanation(
        explicit_disjoint_axioms=_explain_explicit_disjointness(class1, class2),
        cardinality_conflicts=_explain_cardinality_conflicts(class1, class2),
        property_presence_conflicts=_explain_property_presence_conflicts(class1, class2)
    )

def detect_and_explain_incompatibilities(class1, class2):
    """
    Determine if `class1` and `class2` are compatible and
    explain the incompatibilities if they are not.
    """
    is_compatible = check_compatibility(class1, class2)
    if is_compatible:
        print(f"No incompatibilities detected between {class1.name} and {class2.name}.")
    else:
        print(explain_incompatibilities(class1, class2))
