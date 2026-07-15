import owlready2 as owl
import types

onto =  owl.get_ontology("http://example.org/ontology.owl")
with onto:
    A = types.new_class("A", (owl.Thing,))
    B = types.new_class("B", (owl.Thing,))

    class name(owl.DataProperty):
        pass

    A.is_a.extend([name.min(0), name.max(1)])
    B.is_a.extend([name.min(1), name.max(1)])

    # To determine if A->B message transfer is lossy
    # (meaning A can send messages B is not equipped to receive),
    # look at the set difference A-B. If A-B isn't empty,
    # then there are instances of A that cannot be instances of B.
    # In OWL, A-B is implemented as A and not B (A & ~B).
    C = types.new_class("C", (owl.Thing,))
    C.equivalent_to.append(A & ~B)

    owl.sync_reasoner()

    print(not owl.Nothing in C.equivalent_to)
