The `face` subpackage contains:
- Data Model (`types.py`) - a simple data model for representing a subset of FACE Data Models necessary for reasoning
- Transformation (`types.py`) - a transformation from the simplified FACE data model to OWL classes and properties
- I/O (`io.py`) - (TODO) IO functions for importing and exporting FACE Data Models

## Transformation

### FACE Conceptual Ontology
- FACE Entity -> OWL Class
- FACE Observable -> OWL Class
- FACE Characteristic -> OWL ObjectProperty (one per Characteristic) w/ cardinality & range restrictions on Entity class

### FACE Logical Ontology (separate ontology that extends the Conceptual ontology)
- FACE Unit -> OWL Class
- FACE MeasurementSystem -> OWL "MeasurementSystem" class that subclasses an Observable (all disjoint unless convertible)
                         -> OWL ObjectProperty `hasUnit` w/ range restricted to a Unit class
- FACE Logical Entity -> add restriction to exicting Conceptual ObjectProperty that range should be the MeasurementSystem

### FACE Platform Ontology (separate ontology that extends the Platform ontology)
- FACE DatatType -> built-in OWL datatype (e.g., `xsd:integer`, `xsd:string`, etc.)
                 -> OWL DataProperty `hasValue` w/ range restricted to a datatype

#### Example
-- Conceptual
Temperature Observable -> Class `Temperature`
Engine Entity -> OWL class `Engine`
Engine temp Characteristic -> class `Engine` has `hasTemperature` class with range restricted to Temperature and cardinality restriction 1..1
-- Logical
MeasurementSystem TemperatureInDegreesCelsius -> OWL class `TemperatureInDegreesCelsius` (subclass of `MeasurementSystem` and `Temperature`)
                                              -> add required cardinality & `DegreesFahrenheit` range restriction
Entity `MyLogicalEngine` - add `hasTemperature` range restriction `TemperatureInDegreesCelsius`
-- Platform