```mermaid
flowchart LR

  %% DSDM 1 (Green)
  subgraph DSDM1["DSDM 1"]
    direction TB
    style DSDM1 fill:#e6f9e6,stroke:#2e7d32
    MS3[MeasurementSystem3]
    MS3a[MeasurementSystem3a]
    MS3b[MeasurementSystem3b]
    MsgC[EntityC]
    MsgD[EntityD]
    EntityA[EntityA]
    EntityA1[EntityA1]
    EntityA2[EntityA2]
    A_attr1[EntityA_Char1: Characteristic]
    A_attr2[EntityA_Char2: Characteristic]
    A_attr3[EntityA_Char3: Characteristic]
    A_attr4[EntityA_Char4: Characteristic]
    A_attr5[EntityA_Char5: Characteristic]
    A_attr6[EntityA_Char6: Characteristic]
    A_attr7[EntityA_Char7: Characteristic]
    A_attr8[EntityA_Char8: Characteristic]
    A_attr9[EntityA_Char9: Characteristic]
    A_attr10[EntityA_Char10: Characteristic]
    %% MeasurementSystems to Units
    MS3 --> U6
    MS3 --> U7
    MS3a --> U1
    MS3b --> U2
    %% MeasurementSystems to Observables
    MS3 --> Obs6
    MS3 --> Obs7
    MS3 --> Obs8
    MS3a --> Obs1
    MS3b --> Obs2
    %% Entity inheritance
    EntityA1 --> EntityA
    EntityA2 --> EntityA1
    %% EntityA to Characteristics
    EntityA -- "0..*" --> A_attr1
    EntityA -- "1..1" --> A_attr2
    EntityA -- "0..1" --> A_attr3
    EntityA -- "4..4" --> A_attr4
    EntityA -- "0..*" --> A_attr5
    EntityA -- "1..1" --> A_attr6
    EntityA -- "0..1" --> A_attr7
    EntityA -- "4..4" --> A_attr8
    EntityA -- "0..*" --> A_attr9
    EntityA -- "1..1" --> A_attr10
    %% Characteristics to MeasurementSystem or Entity
    A_attr1 --> MS3
    A_attr2 --> EntityA1
    A_attr3 --> MS3a
    A_attr4 --> EntityA2
    A_attr5 --> MS3b
    A_attr6 --> MS3
    A_attr7 --> EntityA
    A_attr8 --> MS3
    A_attr9 --> EntityA1
    A_attr10 --> MS3
    %% Other links
    MsgC --> Obs6
    MsgC --> Obs7
    MsgD --> Obs8
    MsgD --> Obs9
    MsgD --> Obs10
  end

  
  %% FACE SDM (Blue)
  subgraph FACE_SDM["FACE SDM"]
    direction TB
    style FACE_SDM fill:#e3f0fc,stroke:#1976d2
    Obs1[Observable1]
    Obs2[Observable2]
    Obs3[Observable3]
    Obs4[Observable4]
    Obs5[Observable5]
    Obs6[Observable6]
    Obs7[Observable7]
    Obs8[Observable8]
    Obs9[Observable9]
    Obs10[Observable10]
    Obs11[Observable11]
    Obs12[Observable12]
    Obs13[Observable13]
    Obs14[Observable14]
    Obs15[Observable15]
    U1[Unit1]
    U2[Unit2]
    U3[Unit3]
    U4[Unit4]
    U5[Unit5]
    U6[Unit6]
    U7[Unit7]
    U8[Unit8]
    U9[Unit9]
    Dat1[IntegerDatatype]
    Dat2[FloatDatatype]
    Dat3[StringDatatype]
    Dat4[BooleanDatatype]
    Dat5[EnumeratedDatatype]
  end

  %% DSDM 2 (Orange)
  subgraph DSDM2["DSDM 2"]
    direction TB
    style DSDM2 fill:#fff3e0,stroke:#ef6c00
    MS4[MeasurementSystem4]
    MS4a[MeasurementSystem4a]
    MS4b[MeasurementSystem4b]
    MsgE[EntityE]
    MsgF[EntityF]
    EntityB[EntityB]
    EntityB1[EntityB1]
    EntityB2[EntityB2]
    B_attr1[EntityB_Char1: Characteristic]
    B_attr2[EntityB_Char2: Characteristic]
    B_attr3[EntityB_Char3: Characteristic]
    B_attr4[EntityB_Char4: Characteristic]
    B_attr5[EntityB_Char5: Characteristic]
    B_attr6[EntityB_Char6: Characteristic]
    B_attr7[EntityB_Char7: Characteristic]
    B_attr8[EntityB_Char8: Characteristic]
    B_attr9[EntityB_Char9: Characteristic]
    B_attr10[EntityB_Char10: Characteristic]
    %% MeasurementSystems to Units
    MS4 --> U8
    MS4 --> U9
    MS4a --> U3
    MS4b --> U4
    %% MeasurementSystems to Observables
    MS4 --> Obs11
    MS4 --> Obs12
    MS4 --> Obs13
    MS4a --> Obs3
    MS4b --> Obs4
    %% Entity inheritance
    EntityB1 --> EntityB
    EntityB2 --> EntityB1
    %% EntityB to Characteristics
    EntityB -- "0..*" --> B_attr1
    EntityB -- "1..1" --> B_attr2
    EntityB -- "0..1" --> B_attr3
    EntityB -- "4..4" --> B_attr4
    EntityB -- "0..*" --> B_attr5
    EntityB -- "1..1" --> B_attr6
    EntityB -- "0..1" --> B_attr7
    EntityB -- "4..4" --> B_attr8
    EntityB -- "0..*" --> B_attr9
    EntityB -- "1..1" --> B_attr10
    %% Characteristics to MeasurementSystem or Entity
    B_attr1 --> MS4
    B_attr2 --> EntityB1
    B_attr3 --> MS4a
    B_attr4 --> EntityB2
    B_attr5 --> MS4b
    B_attr6 --> MS4
    B_attr7 --> EntityB
    B_attr8 --> MS4
    B_attr9 --> EntityB1
    B_attr10 --> MS4
    %% Other links
    MsgE --> Obs11
    MsgE --> Obs12
    MsgF --> Obs13
    MsgF --> Obs14
    MsgF --> Obs15
  end

  %% Compatibility arrow
  EntityA <-->|"compatible?"| EntityB
  style EntityA fill:#f00
  style EntityB fill:#f00
 ```