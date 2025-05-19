"""
Core FACE data model. Defines the minimal representation of FACE concepts needed for reasoning about compatibility.
"""
import attrs
import typing as ty

from pydmsd.ontology.types import Ontology


@attrs.define
class Characteristic:
    name: str
    lower_bound: int
    upper_bound: int
    value_type: ty.Any


class Observable:
    def __init__(self, name: str, model: "FaceDataModel"):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_class(name)


class Entity:
    def __init__(self, name: str, model: "FaceDataModel"):
        self.name = name
        self.model = model
        self.characteristics = []

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_class(name)

    def create_characteristic(self, name, lower_bound, upper_bound, value_type):
        char = Characteristic(name, lower_bound, upper_bound, value_type)
        self.characteristics.append(char)

        # Create the underlying ontology property and restrictions
        prop = self.model.ontology.define_object_property(f"{self.name}.{name}", range_=value_type.ontology_class)
        range_type = value_type.ontology_class.owl_cls

        if lower_bound == upper_bound:
            self.ontology_class.add_exactly_cardinality(prop, lower_bound, range_type)
        else:
            self.ontology_class.add_min_cardinality(prop, lower_bound, range_type)
            self.ontology_class.add_max_cardinality(prop, upper_bound, range_type)

        return char


class FaceDataModel:
    def __init__(self):
        self.entities = []
        self.observables = []
        self.ontology = Ontology()

    def create_entity(self, name: str):
        entity = Entity(name, model=self)
        self.entities.append(entity)
        return entity

    def create_observable(self, name: str):
        observable = Observable(name, model=self)
        self.observables.append(observable)
        return observable
