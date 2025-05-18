from pydmsd.face.types import FaceDataModel
from pydmsd.ontology import reasoner

model = FaceDataModel()

USPatient = model.create_entity("USPatient")
NHSPatient = model.create_entity("NHSPatient")

# USPatient has required social security number
USPatient.create_characteristic(name="ssn", lower_bound=1, upper_bound=1, value_type=str)

# check compatibility
reasoner.detect_and_explain_incompatibilities(NHSPatient, USPatient)
