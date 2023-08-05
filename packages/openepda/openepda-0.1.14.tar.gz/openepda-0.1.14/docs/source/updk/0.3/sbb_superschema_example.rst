.. code-block:: yaml

  # Snippets of the SBB superschema showing the metadata labels in action.

  blocks:
    ...
      ...
      <block_name>:
        ...
          ...
          pins:
            _type: object
            _required: true
            _doc: Contains one or more pin definitions for <block_name>.
            _properties:
              <pin_name>:
                _type: object
                _required: true
                _doc: Define a pin named <pin_name>.
                _properties:
                  width:
                    _type: float
                    _required: true
                    _doc: Width of the pin.
                    _example: 2.0
                  width_unit:
                     _type: str
                     _required: false
                     _doc: Unit of the pin width.
                     _allowed_values: list of allowed values
                     _default: um   
                     _example: um
                  ...
          drc:
            _type: object
            _required: true
            _doc: Define zero or more DRC rules.
            _default: null
            _properties:
              drc_rules:
                _type: subschema
                _required: false
                _doc: drc rules
          
