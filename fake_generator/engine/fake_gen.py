import pandas as pd 
from faker import Faker
from fake_generator.engine.custom_provider import CustomProvider

class FakeGenerator():
    def __init__(self, schema_list : str, seed : int = 123, custom_provider : CustomProvider = None):
        self.schema_list : list = schema_list
        self.seed = seed
        self.custom_provider : CustomProvider = custom_provider

    @property
    def set_seed(self, seed):
        self.seed = seed
    
    def generate_fake_columns(self, schema : dict, num_rows: int) -> list:
        """ Generate fake data for one column
        Args:
            schema :containing schema {column name, category, type, unique}
            num_rows : number of rows to generate
        Returns:
            list of values based on the faker category 
        """
        faker = Faker()
        Faker.seed(self.seed)
        faker.add_provider(self.custom_provider)
        return list(map(lambda x: getattr(faker, schema['category'])() , range(num_rows)))
        
    def generate_fake_data(self, num_rows) -> pd.DataFrame:
        """ Generate Fake data based on schema
        """
        data_columns = list(map(lambda schema, num_rows: self.generate_fake_columns(schema, num_rows), self.schema_list, [num_rows] * num_rows))
        data_columns = list(zip(*data_columns))
        fake_data = pd.DataFrame(data_columns, columns=[schema['column'] for schema in self.schema_list])
        return fake_data
