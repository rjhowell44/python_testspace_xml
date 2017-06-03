from python_testspace_xml import testspace_xml
import pytest
import os
from lxml import etree, objectify
from lxml.etree import XMLSyntaxError


def create_simple_testspace_xml(self):
    testspace_report = testspace_xml.TestspaceReport()
    example_suite = testspace_report.get_or_add_suite('Example Suite')

    test_case = testspace_xml.TestCase('test passing', 'passed')
    example_suite.add_test_case(test_case)

    test_case = testspace_xml.TestCase('test failed', 'failed')
    example_suite.add_test_case(test_case)

    test_case = testspace_xml.TestCase('test in_progress', 'in_progress')
    example_suite.add_test_case(test_case)

    test_case = testspace_xml.TestCase('test not_applicable', 'not_applicable')
    example_suite.add_test_case(test_case)

    test_case = testspace_xml.TestCase('test passing 2', 'passed')
    example_suite.add_test_case(test_case)

    #test_case.add_text_annotation("annotation 1", description="This is a test case annotation")

    testspace_report.xml_file('testspace.xml')

    xml_file = open('testspace.xml', 'r')
    self.testspace_xml_string = xml_file.read()
    self.testspace_xml_root = etree.fromstring(self.testspace_xml_string)
    xml_file.close()


class TestTestspaceXml:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        create_simple_testspace_xml(self)

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        os.remove('testspace.xml')

    def test_number_passed_testcases(self):
        assert 'passed="2"' in self.testspace_xml_string
        test_suite = self.testspace_xml_root.xpath('//test_suite')
        num_passed = int(test_suite[0].get('passed'))
        assert num_passed is 2

    def test_number_failed_testcases(self):
        assert 'passed="2"' in self.testspace_xml_string
        test_suite = self.testspace_xml_root.xpath('//test_suite')
        num_passed = int(test_suite[0].get('failed'))
        assert num_passed is 1

    def test_number_in_progress_testcases(self):
        assert 'passed="2"' in self.testspace_xml_string
        test_suite = self.testspace_xml_root.xpath('//test_suite')
        num_passed = int(test_suite[0].get('in_progress'))
        assert num_passed is 1

    def test_number_not_applicable_testcases(self):
        assert 'passed="2"' in self.testspace_xml_string
        test_suite = self.testspace_xml_root.xpath('//test_suite')
        num_passed = int(test_suite[0].get('not_applicable'))
        assert num_passed is 1

    def test_validate_xsd(self):
        assert xml_validator(self.testspace_xml_string, 'tests/report_v1.xsd')


def xml_validator(some_xml_string, xsd_file):
    try:
        schema = etree.XMLSchema(file=xsd_file)
        parser = objectify.makeparser(schema=schema)
        objectify.fromstring(some_xml_string, parser)
    except XMLSyntaxError:
        # handle exception here
        return False
    return True
