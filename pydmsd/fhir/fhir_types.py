"""
Core FHIR data model. Defines the minimal representation of FHIR concepts needed for reasoning about compatibility.
"""
import attrs
import typing as ty

from pydmsd.ontology.types import Ontology
from pydmsd.fhir.download import fetch_and_parse_fhir_resource, RawFhirResource


class Datatype:
    def __init__(self, name: str, model: "FhirDataModel"):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_observable(name)


class Resource:
    def __init__(self, name: str, model: "FhirDataModel"):
        self.name = name
        self.model = model

        # Create the underlying ontology class
        self.ontology_class = self.model.ontology.define_class(name)

    def create_element(self, name, lower_bound, upper_bound, value_type):
        """Each FHIR element maps to both a DMSD observable and and a DMDS property"""
        # Create the underlying DMSD observable
        # TODO is a period OK or does this need to be an underscore?
        prop = self.model.ontology.define_observable(f"{self.name}.{name}")

        # Create the underlying ontology property and restrictions
        owl_prop = self.model.ontology.define_object_property(f"{self.name}.{name}", range_=value_type.ontology_class)
        owl_range_type = value_type.ontology_class.owl_cls

        if lower_bound and upper_bound and lower_bound == upper_bound:
            self.ontology_class.add_exactly_cardinality(owl_prop, lower_bound, owl_range_type)
        elif lower_bound:
            self.ontology_class.add_min_cardinality(owl_prop, lower_bound, owl_range_type)
        elif upper_bound:
            self.ontology_class.add_max_cardinality(owl_prop, upper_bound, owl_range_type)


class FhirDataModel:
    def __init__(self):
        self.entities = {}
        self.ontology = Ontology()

    def create_resource(self, name: str):
        resource = Resource(name, model=self)
        self.entities[name] = resource
        return resource

    def create_datatype(self, name: str):
        datatype = Datatype(name, model=self)
        self.entities[name] = datatype
        return datatype

    def create_resource_from_uri(self, uri: str):
        """Create a resource from a FHIR StructureDefinition URI."""
        raw_resource: RawFhirResource = fetch_and_parse_fhir_resource(uri)
        resource = self.create_resource(raw_resource.name)

        for element in raw_resource.elements:
            lower_bound = int(element.min)
            upper_bound = None if (max := element.max) == "*" else int(max)
            # TODO - not strictly necessary, because repeated class definitions are meaningless in OWL
            datatype = self.entities.get(element.type_name) or self.create_datatype(element.type_name)

            resource.create_element(
                name=element.name,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
                value_type=datatype,
            )

        return resource