import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from fake_generator.engine.fake_gen import FakeGenerator

type = 'string'
schema_list = [ 
    {'column': 'name', 'category': 'name', 'type': type, 'unique': False}, 
    {'column': 'address', 'category': 'address', 'type': type, 'unique': False}, 
    {'column': 'job', 'category': 'job', 'type': type, 'unique': False}, \
    {'column': 'company', 'category': 'company', 'type': type, 'unique': False}, 
]

fake_gen_class = FakeGenerator(schema_list)

class FakeGeneratorTest(unittest.TestCase):

    def test_generate_fake_columns(self):
        # Given
        schema = {'column': 'name', 'category': 'name', 'type': 'string', 'unique': False}
        num_rows = 5
        expected_list = ['Brandon Russell', 'Steven Johnson', 'Evelyn Christian', 'George Cook', 'Aaron Graham']
 
        # When
        value_list = fake_gen_class.generate_fake_columns(schema, num_rows)
        
        # Then
        self.assertEqual(value_list, expected_list)

    def test_generate_fake_data(self):
        # Given
        expected_data = pd.DataFrame({
            'name': {0: 'Brandon Russell', 1: 'Steven Johnson', 2: 'Evelyn Christian', 3: 'George Cook', 4: 'Aaron Graham'},
            'address': {0: '4106 Peterson Center\nEast Matthew, MA 92472', 1: '1961 Leslie Mission\nNorth Christopherberg, DC 03284',
                        2: '747 Kayla Junctions Suite 398\nAlexanderhaven, NE 90263', 3: '658 Melanie Rue Apt. 174\nWest Matthew, MO 10107',
                        4: '503 Marie Lakes Apt. 536\nLake Keithfort, WV 83075'},
            'job': {0: 'Associate Professor', 1: 'Geologist, wellsite', 2: 'Chartered loss adjuster', 3: 'Orthoptist', 4: 'Geographical information systems officer'},
            'company': {0: 'Adams Group', 1: 'Rodriguez-Santana', 2: 'Gray PLC', 3: 'Peterson-Williams', 4: 'Rogers LLC'}}
        )
        
        # When
        num_rows = 5
        fake_data = fake_gen_class.generate_fake_data(num_rows)

        # Then
        assert_frame_equal(fake_data, expected_data)
