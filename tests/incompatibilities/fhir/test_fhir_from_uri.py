import pydmsd.fhir.fhir_types as fhir
import pydmsd.fhir.uri as fhir_uris

fhir_dm = fhir.FhirDataModel()
fhir_dm.create_resource_from_uri(fhir_uris.FHIR_PATIENT_URI)
print("\n".join(map(str, fhir_dm.ontology.owl_ontology.classes())))