"""
Core ontology data model. Abstracts owlready2 to provide basic ontology operations.
"""
from functools import cached_property
import attrs
import collections
import types
import typing as ty
import owlready2 as owl


@attrs.define
class Cardinality:
    min: int = 0
    max: ty.Optional[int] = None  # None means unbounded


class OntologyProperty:
    def __init__(self, name: str, owl_prop: owl.PropertyClass):
        self.name = name
        self.owl_prop = owl_prop


class OntologyClass:
    """Abstracts owlready2 class with basic ontology class operations."""
    def __init__(self, name: str, owl_cls: owl.ThingClass, ontology: 'Ontology'):
        self.name: str = name
        self.owl_cls: owl.ThingClass = owl_cls
        self.ontology: 'Ontology' = ontology

    def add_disjoint_class(self, other: 'OntologyClass') -> None:
        """Declare this class to be disjoint with `other`."""
        with self.ontology.owl_ontology:
            owl.AllDisjoint([self.owl_cls, other.owl_cls])

    def add_equivalent_class(self, other: 'OntologyClass') -> None:
        """Declare this class equivalent to `other`."""
        with self.ontology.own_ontology:
            self.owl_cls.equivalent_to.append(other.owl_cls)

    def add_superclass(self, supercls: 'OntologyClass') -> None:
        """Add a superclass."""
        with self.ontology.owl_ontology:
            self.owl_cls.is_a.append(supercls.owl_cls)

    def add_min_cardinality(self, prop: owl.PropertyClass, cardinality: int, range_type: ty.Optional[owl.ThingClass] = None) -> None:
        """Add a minimum cardinality restriction."""
        with self.ontology.owl_ontology:
            restriction = prop.min(cardinality, range_type)
            self.owl_cls.is_a.append(restriction)

    def add_max_cardinality(self, prop: owl.PropertyClass, cardinality: int, range_type: ty.Optional[owl.ThingClass] = None) -> None:
        """Add a maximum cardinality restriction."""
        with self.ontology.owl_ontology:
            restriction = prop.max(cardinality, range_type)
            self.owl_cls.is_a.append(restriction)

    def add_exactly_cardinality(self, prop: owl.PropertyClass, cardinality: int, range_type: ty.Optional[owl.ThingClass] = None) -> None:
        """Add an exact cardinality restriction."""
        with self.ontology.owl_ontology:
            restriction = prop.exactly(cardinality, range_type)
            self.owl_cls.is_a.append(restriction)

    def add_has_value(self, prop: owl.PropertyClass, value: ty.Any) -> None:
        """Add a hasValue restriction."""
        with self.ontology.owl_ontology:
            restriction = prop.value(value)
            self.owl_cls.is_a.append(restriction)

    def add_only(self, prop: owl.PropertyClass, range_type: owl.ThingClass) -> None:
        """Add an AllValuesFrom (only) restriction."""
        with self.ontology.owl_ontology:
            restriction = prop.only(range_type)
            self.owl_cls.is_a.append(restriction)

    def add_some(self, prop: owl.PropertyClass, range_type: owl.ThingClass) -> None:
        """Add a SomeValuesFrom (some) restriction."""
        with self.ontology.owl_ontology:
            restriction = prop.some(range_type)
            self.owl_cls.is_a.append(restriction)

    @cached_property
    def restrictions(self) -> ty.Set[owl.Restriction]:
        return {r for a in self.owl_cls.ancestors() for r in a.is_a if isinstance(r, owl.Restriction)}

    @cached_property
    def declared_properties(self) -> ty.Set[owl.PropertyClass]:
        """Set of all properties used in restrictions on this class or any of its ancestors."""
        return {r.property for r in self.restrictions}

    @cached_property
    def cardinalities(self) -> ty.Dict[owl.PropertyClass, Cardinality]:
        """
        Constructs map of each property (inherited or explicitly declared) to a (min, max) cardinality tuple
        based on the smallest min and largest max restriction for each property.
        """
        cardinality_map: ty.DefaultDict[owl.PropertyClass, Cardinality] = collections.defaultdict(Cardinality)

        for r in self.restrictions:
            cardinality = cardinality_map[r.property]

            if r.type == owl.MIN and r.cardinality > cardinality.min:
                cardinality.min = r.cardinality
            elif r.type == owl.MAX and cardinality.max is not None and r.cardinality < cardinality.max:
                cardinality.max = r.cardinality
            elif r.type == owl.EXACTLY:
                cardinality.min = cardinality.max = r.cardinality

        return cardinality_map

    @cached_property
    def required_properties(self) -> ty.Set[owl.PropertyClass]:
        """All properties with a min cardinality restriction >= 1"""
        return {p for p, card in self.cardinalities.items() if card.min >= 1}


class Ontology:
    """Abstracts owlready2 ontology with basic ontology operations."""
    def __init__(self, iri: str = "http://example.org/ontology.owl"):
        # Generic
        self.iri: str = iri
        self.owl_ontology: owl.Ontology =  owl.get_ontology(iri)

        # Extand core OWL semantics to name Conceptual, Logical, and Platform concerns
        # Conceptual
        self.observable = self.define_class("Observable")

        # Logical
        self.measurement_system = self.define_class("MeasurementSystem")
        self.unit = self.define_class("Unit")
        self.has_unit = self.define_object_property("hasUnit", domain=self.measurement_system, range_=self.unit)
        # TODO precision, using class hierarchy of precision values for range of hasPrecision object property

        # Platform
        self.integer_value_type = self.define_class("IntegerValueType")
        self.float_value_type = self.define_class("FloatValueType")
        self.double_value_type = self.define_class("DoubleValueType")
        self.string_value_type = self.define_class("StringValueType")
        self.enumeration_value_type = self.define_class("EnumerationValueType")
        self.value_types = [
            self.integer_value_type,
            self.float_value_type,
            self.double_value_type,
            self.string_value_type,
            self.enumeration_value_type
        ]
        #self.declare_all_disjoint(self.value_types)
        self.has_value_type = self.define_object_property(
            "hasValueType",
            domain=self.measurement_system,
            range_=self.value_types)

    def destroy(self, ontology_class):
        owl.destroy_entity(ontology_class.owl_cls)

    def save(self, path, format="rdfxml"):
        """Save the ontology to a file at `path` (default RDF/XML format)."""
        self.owl_ontology.save(file=path, format=format)

    @classmethod
    def load(cls, path):
        """Load an ontology from a file at `path`."""
        owl_ontology = owl.get_ontology(path).load()
        return cls(
            iri=owl_ontology.base_iri,
            owl_ontology=owl_ontology
        )

    # Generic
    def define_class(self, name, parent=None):
        """Define a new ontology class."""
        with self.owl_ontology:
            bases = (parent.owl_cls,) if parent else (owl.Thing,)
            owl_cls = types.new_class(name, bases=bases)
        return OntologyClass(name, owl_cls, self)

    def define_object_property(self, name, domain=None, range_=None):
        """Define a new object property."""
        with self.owl_ontology:
            obj_prop = types.new_class(name, (owl.ObjectProperty,))
            if domain:
                obj_prop.domain = [domain.owl_cls]
            if range_:
                obj_prop.range = [cls.owl_cls for cls in range_] if isinstance(range_, list) else [range_.owl_cls]
        return obj_prop

    def define_data_property(self, name, domain=None, range_=None):
        """Define a new data property."""
        with self.owl_ontology:
            data_prop = types.new_class(name, (owl.DataProperty,))
            if domain:
                data_prop.domain = [domain.owl_cls]
            if range_:
                data_prop.range = [range_] if not isinstance(range_, list) else range_
            return data_prop

    def declare_all_disjoint(self, classes):
        """Declare all classes in `classes` to be disjoint."""
        with self.owl_ontology:
            for cls1, cls2 in zip(classes, classes[1:]):
                cls1.add_disjoint_class(cls2)

    # Conceptual
    def define_observable(self, name):
        return self.define_class(name, parent=self.observable)

    # Logical
    def define_unit(self, name):
        return self.define_class(name, parent=self.unit)

    def define_measurement_system(
            self,
            name,
            observable: OntologyClass,
            unit: OntologyClass,
            value_type: ty.Optional[OntologyClass]=None,
    ) -> OntologyClass:
        ms = self.define_class(name, parent=self.measurement_system)
        ms.add_superclass(observable)
        ms.add_exactly_cardinality(self.has_unit, 1, unit.owl_cls)
        ms.add_only(self.has_unit, unit.owl_cls)
        if value_type:
            ms.add_exactly_cardinality(self.has_value_type, 1, value_type.owl_cls)
        return ms
