.. code-block:: yaml

    # openEPDA CDF
    _openEPDA:
      format: openEPDA-CDF
      version: "0.3"
      link: "https://openEPDA.org"

    cdf: SP19-34
    cell: SP19-34
    unit: um

    bbox:
      - [-50, -50]
      - [4550, 3950]

    fiducial:
      target:
        fidt0: [2250, 257.5]
        fidt1: [2250, 3642.5]
      cornerUL:
        cul0: [1737.5, 257.5]
        cul1: [1737.5, 3642.5]
      disc:
        dsk0: [1500.0, 1500.0]

    io:
      optical_port:
        ioW001: [-50, 25]
        ioW003: [-50, 50]
        ioW005: [-50, 75]
        ioW007: [-50, 100]
        ioW009: [-50, 125]
        ioE001: [4550, 25]
        ioE003: [4550, 50]
        ioE005: [4550, 75]
        ioE007: [4550, 100]
        ioE009: [4550, 125]
      dc_pad:
        dc0N00: [4350, 3845]
        dc0N01: [4200, 3845]
        dc0S00: [150, 55]
        dc0S01: [300, 55]
      rf_pad:
        rf0W00: [150, 1200]
