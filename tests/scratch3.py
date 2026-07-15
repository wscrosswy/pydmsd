import owlready2 as owl
import types

onto =  owl.get_ontology("http://example.org/ontology.owl")
with onto:
    A = types.new_class("A", (owl.Thing,))
    B = types.new_class("B", (owl.Thing,))

    class name(owl.DataProperty):
        pass

    A.is_a.append(name.min(1))
    B.is_a.append(name.min(5))


    # I want to prove that A is not a subclass of B.
    # This would show that there is an instance of A
    # that is not an instance of B.

    # To do that I'm going to construct a subclass of A that's
    # restricted to the cardinality that B can't have.
    # To do that, we'll create a new class A_closed,
    # and if the min of P in B is larger than the min of P in A,
    # we'll add a max restriction that's one less to A_closed.
    # Then the intersection of that class and B will be
    # empty if there was ever an individual that could've existed in A
    # but not in B.
    # Examples:
    # A: name min 2
    # B: name min 5
    # -> A_closed: name max 4
    # --> A_closed & B will be inferred empty
    #
    # A: name min 5
    # B: name min 2
    # -> A_closed: pass
    # --> A_closed & B will not be inferred empty


    C = types.new_class("C", (A,B,))
    #C.is_a.append(name.max(4))

    owl.sync_reasoner()
    print(owl.Nothing in C.equivalent_to)