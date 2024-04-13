from fake_generator.enginefake_gen import FakeGenerator

if __name__ == "__main__":
    print('Generate Fake Data')
    num_rows = 5000
    schema_list = [
    {'column': 'name', 'category': 'name', 'type': type, 'unique': False},
    {'column': 'address', 'category': 'address', 'type': type, 'unique': False},
    {'column': 'job', 'category': 'job', 'type': type, 'unique': False},
    {'column': 'company', 'category': 'company', 'type': type, 'unique': False},
    ]

    print('Parameters')
    print(f'num_rows : {num_rows}')
    print(f'schema list: {schema_list}')
    fake_gen = FakeGenerator(num_rows, schema_list)
    fake_data = fake_gen.generate_fake_data()
    print(fake_data.head())