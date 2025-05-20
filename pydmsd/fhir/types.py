"""
Core FHIR data model. Defines the minimal representation of FHIR concepts needed for reasoning about compatibility.
"""
import attrs
import typing as ty

from pydmsd.ontology.types import Ontology

@attrs.define
class Property:
    name: str
    lower_bound: int
    upper_bound: int
    value_type: ty.Any


class Datatype:
    def __init__(self, name: str, model: "FhirDataModel"):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_class(name)


class Resource:
    def __init__(self, name: str, model: "FhirDataModel"):
        self.name = name
        self.model = model
        self.properties = []

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_class(name)

    def create_property(self, name, lower_bound, upper_bound, value_type):
        prop = Property(name, lower_bound, upper_bound, value_type)
        self.properties.append(prop)

        # Create the underlying ontology property and restrictions
        owl_prop = self.model.ontology.define_object_property(f"{self.name}.{name}", range_=value_type.ontology_class)
        owl_range_type = value_type.ontology_class.owl_cls

        if lower_bound and upper_bound and lower_bound == upper_bound:
            self.ontology_class.add_exactly_cardinality(owl_prop, lower_bound, owl_range_type)
        elif lower_bound:
            self.ontology_class.add_min_cardinality(owl_prop, lower_bound, owl_range_type)
        elif upper_bound:
            self.ontology_class.add_max_cardinality(owl_prop, upper_bound, owl_range_type)

        return prop


class FhirDataModel:
    def __init__(self):
        self.resources = []
        self.ontology = Ontology()

    def create_resource(self, name: str):
        resource = Resource(name, model=self)
        self.resources.append(resource)
        return resource
