from pydmsd.ontology.types import Ontology, Cardinality


def test_ontology_class():
    ontology = Ontology("foo")
    cls_a = ontology.define_class("Class_A")
    cls_b = ontology.define_class(name="Class_B", parent=cls_a)
    dp_a = ontology.define_data_property(name="DataProperty_A")
    cls_a.add_min_cardinality(dp_a, 1)

    assert cls_a.declared_properties == {dp_a}
    assert cls_a.cardinalities == {dp_a: Cardinality(1, None)}
    assert cls_a.required_properties == {dp_a}
    assert cls_b.required_properties == {dp_a}

    dp_a_duplicate = ontology.define_data_property(name="DataProperty_A")
    assert dp_a == dp_a_duplicate
