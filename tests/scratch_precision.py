import owlready2
import owlready2 as owl
import types

onto =  owl.get_ontology("http://example.org/ontology.owl")
with onto:
    A = types.new_class("A", (owl.Thing,))
    B = types.new_class("B", (owl.Thing,))

    class precision(owl.DataProperty):
        pass

    A.is_a.extend([precision.exactly(1), precision.only(owl.ConstrainedDatatype(float, max_inclusive=1))])
    B.is_a.extend([precision.exactly(1), precision.only(owl.ConstrainedDatatype(float, max_inclusive=2))])
    class C(owl.Thing):
        pass

    # check if A-B is non-empty
    # (i.e. there are elements of A that cannot exist in B)
    # I EXPECDT THIS TO BE FALSE
    C.equivalent_to.append(A & ~B)
    owl.sync_reasoner()
    print(not owl.Nothing in C.equivalent_to)

    A2 = types.new_class("A2", (owl.Thing,))
    B2 = types.new_class("B2", (owl.Thing,))
    A2.is_a.extend([precision.exactly(1), precision.only(owl.ConstrainedDatatype(float, max_inclusive=2))])
    B2.is_a.extend([precision.exactly(1), precision.only(owl.ConstrainedDatatype(float, max_inclusive=1))])
    class C2(owl.Thing):
        pass

    # check if A2-B2 is non-empty
    # (i.e. there are elements of A2 that cannot exist in B2)
    # I EXPECT THIS TO BE TRUE
    C2.equivalent_to.append(A2 & ~B2)
    owl.sync_reasoner()
    print(not owl.Nothing in C2.equivalent_to)
