import unittest
from XmlElement import XmlElement as X


class TestMethods(unittest.TestCase):
    test_xml = '<DMSQuery><Archive name="Patient"><ObjectType name="Patient" type="FOLDER"><Fields field_schema="DEF"><Field name="Name" /><Field name="Vorname" /><Feld name="PLZ" /><Field name="Ort">Example Value</Field></Fields></ObjectType></Archive></DMSQuery>'

    def test_create_serialize(self):
        test_xml_element = X('DMSQuery', s=[
            X('Archive', {'name': 'Patient'}, [
                X('ObjectType', {'name': 'Patient', 'type': 'FOLDER'}, [
                    X('Fields', {'field_schema': 'DEF'}, [
                        X('Field', {'name': 'Name'}),
                        X('Field', {'name': 'Vorname'}),
                        X('Feld', {'name': 'PLZ'}),
                        X('Field', {'name': 'Ort'}, t='Example Value')
                    ])
                ])
            ])
        ])
        self.assertEqual(TestMethods.test_xml, test_xml_element.to_string())


    def test_deserialize_serialize(self):
        print(X.from_string(TestMethods.test_xml).to_string())
        print(TestMethods.test_xml)
        self.assertEqual(X.from_string(TestMethods.test_xml).to_string(), TestMethods.test_xml)


    def test_find_findall_append(self):
        test_xml_element = X('DMSQuery', s=[
            X('Archive', {'name': 'Patient'}, [
                X('ObjectType', {'name': 'Patient', 'type': 'FOLDER'}, [
                    X('Fields', {'field_schema': 'DEF'}, [
                        X('Field', {'name': 'Name'}),
                        X('Field', {'name': 'Vorname'}),
                        X('Feld', {'name': 'PLZ'}),
                    ])
                ])
            ])
        ])
        test_xml_element.find().findall()[0].find('Fields').append(X('Field', {'name': 'Ort'}, t='Example Value'))
        self.assertEqual(TestMethods.test_xml, test_xml_element.to_string())


    def test_attribs(self):
        test_xml_element = X('DMSQuery', s=[
            X('Archive', {'name': 'Patient'}, [
                X('ObjectType', {'name': 'Patient', 'type': 'FOLDER'}, [
                    X('Fields', {'field_schema': 'DEF'}, [
                        X('Field', {'name': 'Name'}),
                        X('Field', {'name': 'Vorname', 'internal_name': 'FirstName'}, t='Test'),
                        X('Feld', {'name': 'PLZ'}),
                    ])
                ])
            ])
        ])
        self.assertEqual(test_xml_element.Archive[0].ObjectType[0].Fields[0].Field[1].text, 'Test')
        self.assertEqual(test_xml_element.Archive[0].ObjectType[0].Fields[0].Field[1].name, 'Field') # the xml attribute 'name' cannot be access by .-operator shorthand
        self.assertEqual(test_xml_element.Archive[0].ObjectType[0].Fields[0].Field[1].internal_name, 'FirstName')


if __name__ == '__main__':
    unittest.main()