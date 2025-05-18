from pydmsd.face.types import FaceDataModel
from pydmsd.ontology import reasoner

model = FaceDataModel()

Helicopter = model.create_entity("Helicopter")
Quadrotor = model.create_entity("Quadrotor")

# Helicopter has 1 rotor
Helicopter.create_characteristic(name="rotorSpeed", lower_bound=1, upper_bound=1, value_type=float)

# Quadrotor has 4 rotors
Quadrotor.create_characteristic(name="rotorSpeed", lower_bound=4, upper_bound=4, value_type=float)

# Quadrotor has a National Quadrotors Association ID
Quadrotor.create_characteristic(name="nqaid", lower_bound=1, upper_bound=1, value_type=str)

# check compatibility
is_compatible = reasoner.check_compatibility(Helicopter, Quadrotor)

# explain compatibility
if not is_compatible:
    print(reasoner.explain_incompatibilities(Helicopter, Quadrotor))
