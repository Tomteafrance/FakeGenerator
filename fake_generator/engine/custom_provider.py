from faker import Faker
from faker.providers import BaseProvider

class CustomProvider:
    
    @classmethod
    def id_class(cls):
        faker = Faker()
        return faker.pystr_format("#####{{random_int}}") 
    
    @classmethod
    def account_currency(cls):
        faker = Faker()
        return faker.pystr(max_chars = 3).upper()

    @classmethod
    def ten_letters(cls):
        faker = Faker()
        return faker.pystr(max_chars = 10).upper()
    
    @classmethod
    def two_letters(cls):
        faker = Faker()
        return faker.pystr(max_chars = 2).upper()
    
    @classmethod
    def one_letter(cls):
        faker = Faker()
        return faker.pystr(max_chars = 1).upper()
    
    @classmethod
    def num_compte(cls):
        faker = Faker()
        return faker.country_code() + str(random_with_N_digits(25))
