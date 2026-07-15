```mermaid
flowchart TD

  subgraph SDM["SDM"]
    direction TB
    Observable1[Observable1]
    Unit1[Unit1]
    Unit2[Unit2]
    MeasurementA[MeasurementA]
    MeasurementB[MeasurementB]
  end

  EntityA[EntityA]
  EntityB[EntityB]
  CharA[CharA: Characteristic]
  CharB[CharB: Characteristic]

  EntityA -- "0..1" --> CharA
  EntityB -- "1..1" --> CharB

  CharA --> MeasurementA
  CharB --> MeasurementB

  MeasurementA --> Unit1
  MeasurementB --> Unit2
  MeasurementA --> Observable1
  MeasurementB --> Observable1
 ```