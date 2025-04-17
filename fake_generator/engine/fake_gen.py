from typing import List, Dict, Optional, Any
import warnings
from tqdm import tqdm
import pandas as pd 
from faker import Faker
from faker.exceptions import UniquenessException
from fake_generator.engine.custom_provider import CustomProvider

class FakeGenerator():
    def __init__(self, schema_list: List[Dict[str, Any]], seed : int = 123, custom_provider: Optional[Any] = None, local: str = 'en_US'):
        self.schema_list = schema_list
        self.seed = seed
        self.custom_provider = custom_provider
        self.local = local
        self.faker = Faker(self.local)

        if custom_provider:
            self.faker.add_provider(custom_provider)

        self.faker.seed(self.seed)
        self._validate_schema()

    def _validate_schema(self):

        required_keys = {'column', 'category'}
        for schema in self.schema_list:
            missing = required_keys - schema.keys()
            if missing:
                raise ValueError(f"Schema {schema} missing keys : {missing}")
            if not hasattr(self.faker, schema['category']):
                raise AttributeError(f"Category {schema['category']} does't exist")
            
    def set_seed(self, seed: int):
        """ Reinitialize the seed for the fake generator
        """
        self.seed = seed
        self.faker.seed(self.seed)
    
    def _generate_column_data(self, schema: Dict, num_rows: int) -> List:
        method = getattr(self.faker, schema['category'])
        unique = schema.get('unique', False)
        kwargs = schema.get('kwargs', {})
        data_type = schema.get('type')

        values = []
        for _ in range(num_rows):
            try:
                value = method(**kwargs) if not unique else self.faker.unique.__getattr__(schema['category'])(**kwargs)
                
                if data_type:
                    if data_type == 'datetime':
                        value = pd.to_datetime(value)
                    else:
                        value = __builtins__[data_type](value)
                        
                values.append(value)
            except UniquenessException:
                warnings.warn(f"Unique values exhausted for {schema['category']}, duplicates allowed")
                self.faker.unique.clear()
                values.append(method(**kwargs))

        return values

    def generate_dataframe(self, num_rows: int, show_progress: bool = False) -> pd.DataFrame:
        columns = {}
        iterator = tqdm(self.schema_list, desc="Generating data") if show_progress else self.schema_list

        for schema in iterator:
            columns[schema['column']] = self._generate_column_data(schema, num_rows)

        return pd.DataFrame(columns)

    def stream_data(self, batch_size: int = 1000):
        """ Streaming Generation
        """
        while True:
            yield self.generate_dataframe(batch_size)

    # Nouvelle fonctionnalité : Validation des données
    def validate_data(self, df: pd.DataFrame) -> bool:
        """ Validate Dataframe
        """
        for schema in self.schema_list:
            col = schema['column']
            if schema.get('type'):
                if not df[col].apply(type).eq(__builtins__[schema['type']]).all():
                    return False
            if schema.get('unique') and not df[col].is_unique:
                return False
        return True
    
    def generate_data_profile(self, df: pd.DataFrame) -> Dict:
        """ Generate statistique for the fake data
        """
        return {
            'missing_values': df.isna().sum().to_dict(),
            'value_distributions': {
                col: df[col].value_counts().to_dict() for col in df.columns
            }
        }
    
    def add_pattern_column(self, pattern: str, column_name: str):
        """Add pattern for a column with custom regex"""
        self.faker.add_provider(RegexProvider)
        self.schema_list.append({
            'column': column_name,
            'category': 'regex',
            'kwargs': {'pattern': pattern}
        })

if __name__ == "__main__":
    schema = [
        {
            "column": "email",
            "category": "email",
            "type": "str",
            "unique": True
        },
        {
            "column": "birthdate",
            "category": "date_of_birth",
            "type": "datetime",
            "kwargs": {"minimum_age": 18, "maximum_age": 90}
        }
    ]

    generator = FakeGenerator(schema, locale='fr_FR')
    df = generator.generate_dataframe(1000, show_progress=True)
    print(df.head())
    print("Data valid?", generator.validate_data(df))