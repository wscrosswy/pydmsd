import requests
import json
import typing as ty


def download_fhir_structuredefinition(uri):
    """Download FHIR StructureDefinition JSON from a canonical URI."""
    headers = {"Accept": "application/json"}
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
    return response.json()

# All FHIR resources inherit these elements from DomainResource,
# which we ignore for compatibility checking
IGNORED_ELEMENT_SUFFIXES = (
    ".id",
    ".meta",
    ".implicitRules",
    ".language",
    ".text",
    ".contained",
    ".modifierExtension",
)

class RawFhirElement(ty.NamedTuple):
    name: str
    min: int
    max: str
    type_name: str

class RawFhirResource(ty.NamedTuple):
    name: str
    elements: ty.List[RawFhirElement]

def value_set_from_uri(uri):
    """
    Extract the value set name from a URI.
    Example: http://hl7.org/fhir/ValueSet/administrative-gender|5.0.0 - administrative-gender
    """
    return uri.rsplit("/", 1)[-1].split("|", 1)[0]

def parse_structuredefinition(struct_def_json):
    """Extract relevant info from FHIR StructureDefinition JSON."""
    resource_name = struct_def_json["name"]
    base_type_name = struct_def_json["type"]
    raw_elements = struct_def_json.get("snapshot", {}).get("element", [])

    elements = []
    for i, elem in enumerate(raw_elements):
        # for some reason FHIR includes the base type as an element of itself
        if elem["path"] == base_type_name:
            continue

        # skip elements that all resources inherit from DomainResource
        if elem["path"].endswith(IGNORED_ELEMENT_SUFFIXES):
            continue

        # handle extensions
        if elem["path"].endswith("extension"):
            # for some reason FHIR names an set of extensions as an element of itself
            if elem.get("sliceName") is None:
                continue
            else:
                element_name = elem["sliceName"]
        else:
            element_name = elem["path"].replace(".", "_")[len(base_type_name) + 1:]


        if (binding := elem.get("binding")) is not None:
            element_type_name = value_set_from_uri(binding["valueSet"])
        else:
            # LIMITATION - NOT HANDLING MULTIPLE TYPES
            element_type_field = elem["type"][0]

            # handle references to other resources
            if (resource_ref_name := element_type_field.get("targetProfile")) is not None:
                # LIMITATION - NOT HANDLING INTER-RESOURCE REFERENCES
                # element_type_name = resource_ref_name[0].rsplit("/")[-1]
                continue
            # handle extensions
            elif element_type_field["code"] == "Extension":
                # LIMITATION - NOT ALL  EXTENSION FORMATS SUPPORTED
                try:
                    element_type_name = value_set_from_uri(element_type_field["profile"][0])
                except:
                    continue
            else:
                element_type_name = element_type_field["code"]

        # LIMITATION - NOT SUPPORTING BackboneElement
        if element_type_name == "BackboneElement":
            continue

        elements.append(
            RawFhirElement(
                name=element_name,
                min=elem["min"],
                max=elem["max"],
                type_name=element_type_name,
            )
        )

    return RawFhirResource(
        name=resource_name,
        elements=elements
    )

def fetch_and_parse_fhir_resource(uri):
    """Download and parse a FHIR resource from its canonical URI."""
    struct_def = download_fhir_structuredefinition(uri)
    return parse_structuredefinition(struct_def)

if __name__ == "__main__":
    # example
    from pydmsd.fhir.uris import FHIR_US_CORE_PATIENT
    uri = FHIR_US_CORE_PATIENT
    fhir_profile = fetch_and_parse_fhir_resource(uri)
    print(json.dumps(fhir_profile, indent=2))
