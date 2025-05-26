"""
Core FACE data model. Defines the minimal representation of FACE concepts needed for reasoning about compatibility.
"""
import attrs
import typing as ty

from pydmsd.ontology.types import Ontology, OntologyProperty


class FaceElement:
    def __init__(self, name: str, model: "FaceDataModel"):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_observable(name)


class Observable:
    def __init__(self, name: str, model: "FaceDataModel"):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_observable(name)


# Conceptual


class Entity:
    def __init__(self, name: str, model: "FaceDataModel"):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_class(name)


    def create_characteristic(self, name, lower_bound, upper_bound, value_type):
        # Create the underlying ontology property and restrictions
        owl_prop = self.model.ontology.define_object_property(f"{self.name}.{name}", range_=value_type.ontology_class)

        owl_range_type = value_type.ontology_class.owl_cls

        if lower_bound and upper_bound and lower_bound == upper_bound:
            self.ontology_class.add_exactly_cardinality(owl_prop, lower_bound, owl_range_type)
        elif lower_bound:
            self.ontology_class.add_min_cardinality(owl_prop, lower_bound, owl_range_type)
        elif upper_bound:
            self.ontology_class.add_max_cardinality(owl_prop, upper_bound, owl_range_type)

        return owl_prop

    def create_specialization(self, name: str) -> "Entity":
        """Create a specialization of this entity."""
        specialization = self.model.create_entity(name)
        specialization.ontology_class.add_superclass(self.ontology_class)
        return specialization


# Logical


class Unit:
    def __init__(self, name: str, model: "FaceDataModel"):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_unit(name)


class ValueType:
    def __init__(self, name: str, model: "FaceDataModel"):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define(name)


class MeasurementSystem:
    def __init__(self, name: str, model: "FaceDataModel", unit: Unit, value_type: ValueType):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_measurement_system(name=name, unit=unit, value_type=value_type)


class FaceDataModel:
    def __init__(self):
        self.ontology = Ontology()

    def _create_element(self, cls, name: str):
        element = cls(name, model=self)
        return element

    # Conceptual
    def create_entity(self, name: str) -> Entity:
        return self._create_element(Entity, name)

    def create_observable(self, name: str) -> Observable:
        return self._create_element(Observable, name)

    # Logical
    def create_unit(self, name) -> Unit:
        return self._create_element(Unit, name)

    def create_measurement_system(self, name, observable, unit, value_type=None) -> MeasurementSystem:
        return self.ontology.define_measurement_system(name, observable.ontology_class, unit.ontology_class, value_type.ontology_class if value_type else None)

