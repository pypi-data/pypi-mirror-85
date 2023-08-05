.. code-block:: yaml

    # openEPDA MDF
    _openEPDA:
      format: openEPDA-MDF
      version: "0.2"
      link: "https://openEPDA.org"

    mdf: mmi_measurement_full_v1
    cell: SP19-3-4
    die_rotation: 0
    input_rotated: True

    measurements:
      mmi_perm:
        measurement_module: FastScan5
        measurement_module_settings:
          source: Tunable_laser
          detector: Powermeter
          wvl_sweep: [1450, 1630]
          sweep_speed: 5 # nm/s
          sweep_wvl_step: 0.01 # nm
        pol: [TE, TM]
        ports: product_min

    Reference:
      - ref_south:
          left: ioW008
          right: ioE012
      - ref_north:
          left: ioW298
          right: ioE302

    measurement_sequence:
      - top_mmi:
        - {measurement: mmi_perm, west_ports: [ioW292, ioW290], east_ports: [ioE296, ioE294]}
        - {measurement: mmi_perm, west_ports: [ioW302, ioW304], east_ports: [ioE306, ioE308]}
