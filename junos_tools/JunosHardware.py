from lxml import etree

def parse_chassis_hardware(s):
    """
    Parses output of "show chassis hardware" output in XML format and returns JSON dictionary
    """

    # TODO: Use parser to skip extraneous console output causing errors
    # parser = etree.XMLParser(recover=True)

    # stree = etree.parse(s, parser=parser)
    # serials = stree.findall("//serial-number")

    # tree = etree.fromstring(s)

    root = etree.fromstring(s)
    tree = etree.ElementTree(root)

    items = []
    
    ## TODO: Add for loop for multiple <chassis-inventory> in case single file
    
    chassis_serial = tree.find(".//{*}chassis-inventory/{*}chassis/{*}serial-number").text
    
    serials = tree.findall(".//{*}serial-number")

    for serial in serials: 
        parent = serial.getparent()
        
        serial_number = serial.text

        description = parent.find("./{*}description")
        description = description.text if description is not None else None

        name = parent.find("./{*}name")
        name = name.text if name is not None else None

        model_number = parent.find("./{*}model-number")
        model_number = model_number.text if model_number is not None else None

        part_number = parent.find("./{*}part-number")
        part_number = part_number.text if part_number is not None else None
        
        items.append(dict(
            serial_number=serial_number,
            name=name,
            model_number=model_number,
            description=description,
            parent=chassis_serial if chassis_serial != serial_number else None))

    # TODO: remove "BUILT-IN" entries
    return dict(items=items)

def parse_chassis_hardware_from_file(file):
    """Wrapper for parse_chassis_hardware()"""
    with open(file, "r") as fh:
        return parse_chassis_hardware(fh.read().replace('\n', ''))

def parse_chassis_hardware_from_zip(file):
    # unzip
    # all_items = list()
    # for each file in zip
        # all_items += parse_chassis_hardware_from_file (wrap this in try)

    pass

if __name__ == "__main__":
    import sys
    import json
    print(json.dumps(parse_chassis_hardware_from_file(sys.argv[1])))
