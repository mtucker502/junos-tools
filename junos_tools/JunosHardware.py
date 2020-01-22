from lxml import etree
from lxml.etree import XMLSyntaxError
from .utils import fix_xml, parse_hostname_from_filename, process_zip


def parse_chassis_hardware(data=None, hostname=None, remove_builtins=True):
    """
    Parses output of "show chassis hardware" output in XML format and returns JSON dictionary
    """

    data = fix_xml(data)
    root = etree.fromstring(data)
    tree = etree.ElementTree(root)

    items = []
        
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
            parent=chassis_serial if chassis_serial != serial_number else None,
            hostname=hostname if hostname else "")
            )

    if remove_builtins:
        items = [item for item in items if item["serial_number"] != "BUILTIN"]
    
    return dict(items=items)


def parse_chassis_hardware_from_file(file):
    """Wrapper for parse_chassis_hardware()"""

    hostname = parse_hostname_from_filename(file)

    with open(file, "r") as fh:
        stream = fh.read()
        return parse_chassis_hardware(data=stream, hostname=hostname)


def main():
    import sys
    import json
    from shutil import rmtree
    
    file = sys.argv[1]

    if file.endswith(".zip"):
        files, zip_dir = process_zip(file)
    else:
        files = [file]
    
    output = dict(items=[])
    for f in files:
        try:
            output["items"] += parse_chassis_hardware_from_file(f)["items"]
        except XMLSyntaxError as err:
            output["errors"].append(dict(
                hostname=parse_hostname_from_filename(f),
                error=str(err)
                ))
    
    if zip_dir:
        rmtree(zip_dir)
    
    print(json.dumps(output))

if __name__ == "__main__":
    main()