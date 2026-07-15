import pydmsd.fhir.fhir_types as fhir
from pydmsd.ontology import reasoner

FHIR_PATIENT_URI = "http://hl7.org/fhir/StructureDefinitionPatient"
FHIR_US_CORE_PATIENT = "http://hl7.org/fhir/us/core/StructureDefinition/us-core-patient"
FHIR_UK_CORE_PATIENT = "https://build.fhir.org/ig/HL7-UK/UK-Core-Access/StructureDefinition-UKCore-Patient.json"

# base resource
fhir_dm = fhir.FhirDataModel()
fhir_patient = fhir_dm.create_resource_from_uri(FHIR_PATIENT_URI)

# instantiate patient resource from URL
fhir_us_core_patient = fhir_dm.create_profile_from_uri(FHIR_US_CORE_PATIENT, fhir_patient)
fhir_uk_core_patient = fhir_dm.create_profile_from_uri(FHIR_UK_CORE_PATIENT, fhir_patient)

assert not reasoner.check_compatibility(fhir_us_core_patient, fhir_uk_core_patient)
print(reasoner.explain_incompatibilities(fhir_us_core_patient, fhir_uk_core_patient))



