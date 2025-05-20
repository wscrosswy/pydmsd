from pydmsd.fhir.types import FhirDataModel, Datatype
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
    Patient.create_property("identifier", 0, None, Identifier)
    Patient.create_property("name", 0, None, HumanName)
    Patient.create_property("birthDate", 0, 1, Date)
    Patient.create_property("address", 0, None, Address)
    Patient.create_property("gender", 0, 1, Code)

    # USPatient Profile
    USPatient = model.create_resource("USPatient")
    USPatient.ontology_class.owl_cls.is_a.append(Patient.ontology_class.owl_cls)
    USPatient.create_property("address", 1, None, Address)
    USPatient.create_property("gender", 1, 1, Code)

    # NHSPatient profile
    NHSPatient = model.create_resource("NHSPatient")
    NHSPatient.ontology_class.owl_cls.is_a.append(Patient.ontology_class.owl_cls)
    NHSPatient.create_property("birthDate", 1, 1, Date)

    assert not reasoner.check_compatibility(NHSPatient, USPatient)
    print(reasoner.explain_incompatibilities(NHSPatient, USPatient))
