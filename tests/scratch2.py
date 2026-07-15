import pydmsd.ontology.types as types
import pydmsd.ontology.reasoner as reasoner

ontology = types.Ontology()

A1 = ontology.define_class("A1")
B1 = ontology.define_class("B1")
A2 = ontology.define_class("A2")
B2 = ontology.define_class("B2")
A3 = ontology.define_class("A3")
B3 = ontology.define_class("B3")

P = ontology.define_object_property("P")

A1.add_min_cardinality(P, 1)
B1.add_min_cardinality(P, 1)
A2.add_min_cardinality(P, 0)
B2.add_min_cardinality(P, 1)
A3.add_min_cardinality(P, 1)
B3.add_min_cardinality(P, 0)

print("A1->B1: " + str(reasoner.check_compatibility(A1, B1)))
print(reasoner.explain_incompatibilities(A1, B1))

print("A2->B2: " + str(reasoner.check_compatibility(A2, B2)))
print(reasoner.explain_incompatibilities(A2, B2))

print("A3->B3: " + str(reasoner.check_compatibility(A3, B3)))
print(reasoner.explain_incompatibilities(A3, B3))
