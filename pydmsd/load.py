import itertools
import logging
from pathlib import PurePath
from typing import List, Tuple

from rdflib import Graph
from rdflib.namespace import OWL, RDF, RDFS
from rdflib.term import Node, BNode

from pydmsd.fhir import FHIR, FHIR_US_CORE, ONE, FHIR_US_CORE_PATIENT, Profile
from pydmsd.rdflib_util import ranges_of, pprint_recursive

_LOGGER = logging.getLogger(__name__)

FHIR_TTL_PATH = PurePath("data/fhir.ttl")


def _add_properties_and_objects(g: Graph, s: Node, po_list: List[Tuple[Node, Node]]):
    """
    Adds a tuple (s,p,o) to graph G for every (p,o) in `po_list`.
    """
    for (p, o) in po_list:
        g.add((s, p, o))


def _construct_property_restriction(g: Graph, property_: Node, constraint: Node, value: Node) -> BNode:
    """
    Constructs a bnode in graph g that is a restriction
    on `property`, defined by `consraint` and `value` (e.g. constraint=maxCardinality, value=1)
    """
    bnode = BNode()
    _add_properties_and_objects(
        g=g,
        s=bnode,
        po_list=[
            (RDF.type, OWL.Restriction),
            (OWL.onProperty, property_),
            (constraint, value),
        ]
    )
    return bnode


def _connect_property_ranges(g: Graph):
    """
    FHIR profile analysis require properties and their types (ranges) be connected.
    The existing FHIR ontology does not have this feature - all properties have the generic "fhir:Reference"
    type as their range. The reason for this is the FHIR ontology is designed to roundtrip instances of
    FHIR resources, which simply have generic references (e.g. URIs) to other resources. Validation is
    a separate concern, so this schema information is not captured.

    To support our algorithms, we must modify the FHIR ontology so the range of each property is its
    fhir:Reference.type instead of a generic fhir:Reference.

    LIMITED SCOPE:
    - This only affects `Patient.generalPractitioner`
    - This is just a "simple" version that just uses one type (Practitioner).
      Sometimes FHIR properties can have multiple types and would need to be handled with a union.
      Here is some prototype SPARQL:
            # first create a class that is the expected range of the property
            DELETE WHERE { fhir:Patient.generalPractitioner.range ?p ?o };
            INSERT DATA {
                fhir:Patient.generalPractitioner.range a           owl:Class ;
                                                       owl:unionOf (fhir:Organization fhir:Practitioner fhir:PractitionerRole) .
            };
            # then modify the property so its range is that class (instead of a generic fhir:Reference)
            DELETE WHERE { fhir:Patient.generalPractitioner rdfs:range ?o };
            INSERT DATA {
              fhir:Patient.generalPractitioner rdfs:range fhir:Patient.generalPractitioner.range .
            };
            # finally, modify all uses of the property so they restrict the property using the expected types
            DELETE { ?bnode owl:allValuesFrom ?o }
            WHERE {
                ?bnode a                 owl:Restriction ;
                       owl:onProperty    fhir:Patient.generalPractitioner ;
                       owl:allValuesFrom ?o .
            } ;
            INSERT { ?bnode owl:allValuesFrom fhir:Patient.generalPractitioner.range }
            WHERE {
                ?bnode a                 owl:Restriction ;
                       owl:onProperty    fhir:Patient.generalPractitioner ;
            } ;
            DELETE WHERE { fhir:Patient.generalPractitioner rdfs:range ?o };
            INSERT DATA {
              fhir:Patient.generalPractitioner rdfs:range fhir:Patient.generalPractitioner.range .
            };

    EQUIVALENT SPARQL:
        DELETE WHERE { fhir:Patient.generalPractitioner rdfs:range ?o };
        INSERT DATA {
            fhir:Patient.generalPractitioner rdfs:range fhir:Practitioner .
        };

    """
    # modify the property so its range is the expected type (instead of a generic fhir:Reference)
    fhir_patient_gp = FHIR['Patient.generalPractitioner']
    fhir_practitioner = FHIR['Practitioner']
    _LOGGER.debug(f"Before: {list(ranges_of(g, fhir_patient_gp))}")

    for triple in g.triples((fhir_patient_gp, RDFS.range, None)):
        g.remove(triple)
    g.add((fhir_patient_gp, RDFS.range, fhir_practitioner))

    _LOGGER.debug(f"After: {list(ranges_of(g, fhir_patient_gp))}")


def _add_profile(g: Graph, profile: Profile):
    """
    Adds profiles to the FHIR ontology.
    Currently, these are not full profiles - just enough to illustrate examples.
    """
    _add_properties_and_objects(
        g=g,
        s=profile.node,
        po_list=itertools.chain(
            [(RDFS.subClassOf, profile.base)],
            [(RDFS.subClassOf, _construct_property_restriction(g=g,
                                                               property_=restriction.property_,
                                                               constraint=restriction.constraint,
                                                               value=restriction.value))
             for restriction in profile.restrictions]
        )
    )
    _LOGGER.debug(f"Profile Added:\n{pprint_recursive(g, FHIR_US_CORE_PATIENT.node, 2)}")


def load_fhir() -> Graph:
    g = Graph()
    g.parse(location=FHIR_TTL_PATH, format="ttl")

    _connect_property_ranges(g)
#    _add_profile(g, FHIR_US_CORE_PATIENT)

    return g


if __name__ == "__main__":
    load_fhir()
