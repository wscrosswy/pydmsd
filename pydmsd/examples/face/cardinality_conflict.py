from pydmsd.face.types import FaceDataModel
from pydmsd.ontology import reasoner

model = FaceDataModel()

Helicopter = model.create_entity("Helicopter")
Quadrotor = model.create_entity("Quadrotor")

# Helicopter has 1 rotor
Helicopter.create_characteristic(name="rotorSpeed", lower_bound=1, upper_bound=1, value_type=float)

# Quadrotor has 4 rotors
Quadrotor.create_characteristic(name="rotorSpeed", lower_bound=4, upper_bound=4, value_type=float)

# check compatibility
reasoner.detect_and_explain_incompatibilities(Helicopter, Quadrotor)
