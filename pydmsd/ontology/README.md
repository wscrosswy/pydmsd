# Data Modeling Language

## OWL Model (Manchester Syntax) represented in `types.py`

```manchester
Class: dsdm:Message

Class: dsdm:Observable

ObjectProperty: dsdm:MessageAttribute
  Domain: dsdm:Message
  Range: dsdm:Message or dsdm:Observable

Class: dsdm:Unit

DatatypeProperty: dsdm.hasPrecision
  Domain: dsdm:Measurement
  Range: xsd:float

ObjectProperty: dsdm.hasUnit
  Domain: dsdm:Measurement
  Range: dsdm:Unit


Class: dsdm:Measurement
  SubClassOf:
    dsdm:hasUnit exactly 1,
    dsdm:hasPrecision max 1
    dsdm:hasDatatype exactly 1

Class: dsdm:Datatype

Class: dsdm:IntegerDatatype
  SubClassOf: dsdm:Datatype

Class: dsdm:LongDatatype
  SubClassOf: dsdm:Datatype

Class: dsdm:FloatDatatype
  SubClassOf: dsdm:Datatype

Class: dsdm:DoubleDatatype
  SubClassOf: dsdm:Datatype

Class: dsdm:StringDatatype
  SubClassOf: dsdm:Datatype

Class: dsdm:BooleanDatatype
  SubClassOf: dsdm:Datatype

Class: dsdm:EnumeratedDatatype
  SubClassOf: dsdm:Datatype

DisjointClasses:
  IntegerDatatype,
  FloatDatatype,
  DoubleDatatype,
  StringDatatype,
  BooleanDatatype,
  EnumeratedDatatype
```


# Language Diagram
```mermaid
%%{init: {"theme": "base", "themeVariables": { "background": "#ffffff", "primaryColor": "#e3f0fc", "edgeLabelBackground":"#ffffff", "primaryBorderColor": "#1976d2", "classTextColor": "#1976d2", "fontFamily": "Segoe UI, Arial" }}}%%
classDiagram
    class AttributeRange
    <<abstract>> AttributeRange

    AttributeRange <|-- Message
    AttributeRange <|-- Observable

    Observable <|-- Measurement

    class Message
    class Observable
    class Measurement
    class MessageAttribute {
        lowerBound : int
        upperBound : int
    }
    class Unit
    class Datatype

    Datatype <|-- IntegerDatatype
    Datatype <|-- LongDatatype
    Datatype <|-- FloatDatatype
    Datatype <|-- DoubleDatatype
    Datatype <|-- StringDatatype
    Datatype <|-- BooleanDatatype
    Datatype <|-- EnumeratedDatatype

    class IntegerDatatype
    class LongDatatype
    class FloatDatatype
    class DoubleDatatype
    class StringDatatype
    class BooleanDatatype
    class EnumeratedDatatype

    Message "1" o-- "1..*" MessageAttribute
    MessageAttribute "1" --> AttributeRange : type
    Measurement "1" --> "1" Unit : hasUnit
    Measurement "0..1" --> float : hasPrecision
    Measurement "1" --> "1" Datatype : hasDatatype
```