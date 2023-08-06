.. code-block:: yaml

  # SBB example for describing a layout for a MMI block and a SOA block

  header:
    description: uPDK example of building blocks
    file_version: 0.1
    openEPDA:
      version: openEPDA-uPDK-SBB-v0.2
      link: "https://openEPDA.org"
    schema_license:
      license: CC BY-ND 4.0
      attribution: "openEPDA-uPDK-SBB-v0.2, Copyright (c) 2017-2019, Ronald Broeke"
    pdk_license: null

  blocks:
    mmi:
      bbox: [[0.0, -10.0], [50.0, -10.0], [50.0, 10.0], [0.0, 10.0]]
      doc: "A 1x2 multi-mode interference (MMI) coupler."
      parameters: null
      pins:
        a0:
          doc: optical
          width: 1.5
          xsection: GUIDE
          xya: [0, 0, 180]
        b0:
          doc: optical
          width: 1.5
          xsection: GUIDE
          xya: [50, 2, 0]
        b1:
          doc: optical
          width: 1.5
          xsection: GUIDE
          xya: [50, -2, 0]
      pin_in: a0
      pin_out: b0
      drc: null
    soa:
      bbox: [[0.0, -0.5*width], [length, -0.5*width], [length, 0.5*width], [0, 0.5*width]]
      doc: "A semiconductor optical amplifier (SOA)"
      parameters:
        length:
          doc: "Length of the SOA."
          type: float
          max: 2500.0
          min: 150.0
          value: 400
          unit: um
        width:
          doc: "Waveguide width of the SOA."
          type: float
          max: 5.0
          min: 0.5
          value: 1.0
          unit: um
      pins:
        a0:
          doc: optical
          width: 1.5
          xsection: ACTIVE
          xya: [0, 0, 180]
        b0:
          doc: optical
          width: 1.5
          xsection: ACTIVE
          xya: [length, 0, 0]
      pin_in: a0
      pin_out: b0
      drc:
        angle:
          values: [0, 180]

