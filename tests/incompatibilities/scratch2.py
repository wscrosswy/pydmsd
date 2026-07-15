from pydmsd.face.types import FaceDataModel
from pydmsd.ontology import reasoner
import owlready2 as owl
import types

onto = owl.get_ontology("http://example.org/ontology.owl")

with onto:
    A = types.new_class("A", (owl.Thing,))
    B = types.new_class("B", (owl.Thing,))

    X = types.new_class("X", (owl.Thing,))
    p = types.new_class("p", (owl.ObjectProperty,))

    A.is_a.append(p.exactly(1, X))
    B.is_a.append(p.exactly(4, X))

    C = types.new_class("C", (A, B))

    owl.sync_reasoner()

    print(C.equivalent_to)
