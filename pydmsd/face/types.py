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
        if isinstance(value_type, Entity):
            prop = self.model.ontology.define_object_property(name)
            filler = value_type.ontology_class
        else:
            prop = self.model.ontology.define_data_property(name, range_=[value_type])
            filler = value_type

        if lower_bound == upper_bound:
            self.ontology_class.add_exactly_cardinality(prop, lower_bound, filler)
        else:
            self.ontology_class.add_min_cardinality(prop, lower_bound, filler)
            self.ontology_class.add_max_cardinality(prop, upper_bound, filler)

        return char


class FaceDataModel:
    def __init__(self):
        self.entities = []
        self.ontology = Ontology()

    def create_entity(self, name: str):
        entity = Entity(name, model=self)
        self.entities.append(entity)
        return entity
