from typing import List

import attrs
from attrs import define
from rdflib import Namespace, Literal, XSD, OWL
from rdflib.term import Node


@define
class Restriction:
    property_: Node
    constraint: Node
    value: Node


@define
class Profile:
    node: Node
    base: Node
    restrictions: List[Restriction] = attrs.Factory(list)


FHIR_URI = "http://hl7.org/fhir/"
FHIR = Namespace(FHIR_URI)
FHIR_US_CORE_URI = "http://hl7.org/fhir/us/core/StructureDefinition/"
FHIR_US_CORE = Namespace(FHIR_US_CORE_URI)
FHIR_NHS_URI = "https://fhir.hl7.org.uk/STU3/StructureDefinition/"
FHIR_NHS = Namespace(FHIR_NHS_URI)
ONE = Literal(1, datatype=XSD.integer)


FHIR_US_CORE_PATIENT = Profile(
    node=FHIR_US_CORE["us-core-patient"],
    base=FHIR.Patient,
    restrictions=[
        Restriction(property_=FHIR["Patient.name"], constraint=OWL.maxCardinality, value=ONE),
        Restriction(property_=FHIR_US_CORE["us-core-patient.us_core_birthsex"], constraint=OWL.maxCardinality, value=ONE),
    ]
)

FHIR_NHS_ORGANIZATION = Profile(
    node=FHIR_NHS["CareConnect-Organization-1"],
    base=FHIR.Organization,
)

FHIR_NHS_ORGANIZATION = Profile(
    node=FHIR_NHS["CareConnect-Practitioner-1"],
    base=FHIR.Practitioner,
)

#FHIR_NHS_PATIENT = Profile(
#    node=FHIR_NHS["CareConnect-Patient-1"],
#    base=FHIR.Patient,
#    restrictions=[
#        Restriction(property_=FHIR[""])
#    ]
#)
