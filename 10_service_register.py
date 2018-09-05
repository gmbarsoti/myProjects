import xml.etree.ElementTree as ET

class const_var_neg_tag:
    def __init__(self, byte_position='', bit_length='', bit_position='', value='', description='', demo=''):
        self.byte_position = str(byte_position)
        self.bit_position = str(bit_position)
        self.bit_length = str(bit_length)
        self.value = str(value)
        self.description = str(description)
        self.demo = str(demo)
        self.demo_data = ''


def const_var_neg_tag_builder(element_tag, tag_type, const_var_obj):
    const_var_neg_tag = ET.SubElement(element_tag, tag_type)
    byte_positionElt = ET.SubElement(const_var_neg_tag, 'BytePosition')
    byte_positionElt.text = const_var_obj.byte_position
        
    bit_lengthElt = ET.SubElement(const_var_neg_tag, 'BitLength')
    bit_lengthElt.text = const_var_obj.bit_length
    
    bit_positionElt = ET.SubElement(const_var_neg_tag, 'BitPosition')
    bit_positionElt.text = const_var_obj.bit_position
    
    if tag_type == 'Negative':
        demo_dataElt = ET.SubElement(const_var_neg_tag, 'DemoData')
        demo_dataElt.text = const_var_obj.value # using same position of value to demo_data
    else:
        valueElt = ET.SubElement(const_var_neg_tag, 'Value')
        valueElt.text = '0x' + const_var_obj.value
    
    descriptionElt = ET.SubElement(const_var_neg_tag, 'Description')
    descriptionElt.text = const_var_obj.description
    
    demoElt = ET.SubElement(const_var_neg_tag, 'Demo')
    demoElt.text = const_var_obj.demo


def xml_main_structure(service_name):    
    xml_prolog = '<?xml version="1.0" encoding="ISO-8859-1"?>'
    
    root = ET.Element('TIPS')
    
    serviceElt = ET.SubElement(root, 'Service')
    requestElt = ET.SubElement(serviceElt, 'Request')
    positiveResponseElt = ET.SubElement(serviceElt, 'PositiveResponse')
    negativeResponseElt = ET.SubElement(serviceElt, 'NegativeResponse')
    
    nameElt = ET.SubElement(serviceElt, 'Name')
    nameElt.text = service_name
    
    descriptionElt = ET.SubElement(serviceElt, 'Description')
    
    negativeElt = ET.SubElement(serviceElt, 'Negative')
    negativeElt.text = 'False'
    
    broadcastElt = ET.SubElement(serviceElt, 'Broadcast')
    broadcastElt.text = 'False'

    
    return root


def register_request_service(service_code, root):
    requestElt = root.find('Service').find('Request')
    
    const_var_neg_obj = const_var_neg_tag(0, 8, 0, service_code, 'Request_Service_ID','')
    const_var_neg_tag_builder(requestElt,'Const', const_var_neg_obj)
    
def negative_response_register(service_code, root):
    negative_responseElt = root.find('Service').find('NegativeResponse')
    
    const_var_neg_obj = const_var_neg_tag(0, 8, 0, '7F', 'Service_ID','')
    const_var_neg_tag_builder(negative_responseElt,'Const', const_var_neg_obj)
    
    const_var_neg_obj = const_var_neg_tag(1, 8, 0, service_code, 'Resquest_Service_ID','')
    const_var_neg_tag_builder(negative_responseElt,'Const', const_var_neg_obj)
    
    const_var_neg_obj = const_var_neg_tag(2, 8, 0, '', 'Response_Code','')
    const_var_neg_tag_builder(negative_responseElt,'Negative', const_var_neg_obj)
    
        
def switch(argument):
    switcher = {
        '10': 'StartDiagnosticSession',
        '21': 'ReadDataByLocalIdentifier'
    }
    default_value = 'UnknowService'+argument 
    return switcher.get(argument, default_value) 



service_code = '22'
service_name = ''

service_name = switch(service_code)
    
root = xml_main_structure(service_name)
register_request_service(service_code, root)
negative_response_register(service_code, root)


doc = ET.ElementTree(root)
doc.write('homemade.xml',encoding="ISO-8859-1")

