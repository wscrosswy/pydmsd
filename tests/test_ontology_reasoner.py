import pytest
from pydmsd.ontology.types import Cardinality
from pydmsd.ontology.reasoner import _cardinalities_overlap


@pytest.mark.parametrize(
    "card1, card2, expected",
    [
        (
            Cardinality(),
            Cardinality(),
            True
        ),
        (
            Cardinality(),
            Cardinality(1,1),
            True
        ),
        (
            Cardinality(1,1),
            Cardinality(2,2),
            False
        ),
        (
            Cardinality(2,2),
            Cardinality(1,1),
            False
        ),
        (
            Cardinality(1,3),
            Cardinality(2,4),
            True
        ),
        (
            Cardinality(1,2),
            Cardinality(2,3),
            True
        )
    ]
)
def test_cardinalities_overlap(card1: Cardinality, card2: Cardinality, expected: bool):
    assert _cardinalities_overlap(card1, card2) == expected
