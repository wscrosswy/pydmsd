from pydmsd.fhir.fhir_types import FhirDataModel, Datatype
from pydmsd.ontology import reasoner

def test_patient_profile_incompatibilities():
    model = FhirDataModel()

    # datatypes
    HumanName = Datatype("HumanName", model)
    Identifier = Datatype("Identifier", model)
    Address = Datatype("Address", model)
    Date = Datatype("Date", model)
    Code = Datatype("Code", model)

    # Base Patient resource
    Patient = model.create_resource("Patient")
    Patient.create_element("identifier", 0, None, Identifier)
    Patient.create_element("name", 0, None, HumanName)
    Patient.create_element("birthDate", 0, 1, Date)
    Patient.create_element("address", 0, None, Address)
    Patient.create_element("gender", 0, 1, Code)

    # USPatient Profile
    USPatient = model.create_resource("USPatient")
    USPatient.ontology_class.owl_cls.is_a.append(Patient.ontology_class.owl_cls)
    USPatient.create_element("address", 1, None, Address)
    USPatient.create_element("gender", 1, 1, Code)

    # NHSPatient profile
    NHSPatient = model.create_resource("NHSPatient")
    NHSPatient.ontology_class.owl_cls.is_a.append(Patient.ontology_class.owl_cls)
    NHSPatient.create_element("birthDate", 1, 1, Date)

    assert not reasoner.check_compatibility(NHSPatient, USPatient)
    print(reasoner.explain_incompatibilities(NHSPatient, USPatient))
