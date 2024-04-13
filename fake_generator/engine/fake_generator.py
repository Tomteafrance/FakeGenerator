import pandas as pd 
from faker import Faker
from custom_provider import CustomProvider

class FakeGenerator():
    def __init__(self, num_rows : int, schema_list : str, custom_provider : CustomProvider = None):
        self.num_rows : int = num_rows
        self.schema_list : list = schema_list
        self.custom_provider : CustomProvider = custom_provider

    def generate_fake_columns(self, schema):
        faker = Faker()
        faker.add_provider(self.custom_provider)
        return list(map(lambda x: getattr(faker, schema['category'])() , range(self.num_rows)))
        
    def generate_fake_data(self):
        data_columns = list(map(lambda schema: self.generate_fake_columns(schema), self.schema_list))
        data_columns = list(zip(*data_columns))
        fake_data = pd.DataFrame(data_columns, columns=[schema['column'] for schema in self.schema_list])
        return fake_data
