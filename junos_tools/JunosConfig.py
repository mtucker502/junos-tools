from lxml import etree


class JunosConfig():

    def get_interfaces(self):
        interfaces_list = self.tree.findall('.//interfaces/interface')

        for interface in interfaces_list:
            int_name = interface.find('./name').text
            self.interfaces[int_name] = {}

            if interface.find('./description') is not None:
                int_description = interface.find('./description').text
                self.interfaces[int_name]['description'] = int_description

            units = interface.findall('./unit')
            if len(units)==0:
                if interface.find('.//bundle') is not None:  # AE interface
                    parent = interface.find('.//bundle').text
                elif interface.find('.//parent') is not None:  # RETH interface
                    parent = interface.find('.//parent').text
                self.interfaces[int_name]['parent'] = parent
            else:
                self.interfaces[int_name]['units'] = {}
                for unit in units:
                    if unit.find('./family') is not None:  # make sure the unit has address families configured
                        unit_number = unit.find('./name').text
                        self.interfaces[int_name]['units'][unit_number] = {}
                        if unit.find('.vlan-id') is not None:
                            vlan = unit.find('.vlan-id').text
                            self.interfaces[int_name]['units'][unit_number]['vlan'] = vlan
                        elif unit.find('./description') is not None:
                            unit_description = unit.find('./description').text
                            self.interfaces[int_name]['units'][unit_number]['description'] = unit_description
                        for family in unit.findall('./family'):
                            for child in family.iterchildren():
                                familyName = child.tag
                                self.interfaces[int_name]['units'][unit_number][familyName] = []
                                for addr in child.findall('./address'):
                                    address = addr.find('./name').text
                                    self.interfaces[int_name]['units'][unit_number][familyName].append(address)

    def __init__(self, config):
        self.config = config
        self.interfaces = {}
        self.tree = etree.fromstring(self.config)
