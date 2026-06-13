from faker import Faker
from sqlite3 import connect
from typing import Sequence


def execute_query(query_string:str)->None:
    fake_db_connection = connect('db.sqlite3')
    fake_db_cursor = fake_db_connection.cursor()

    fake_db_cursor.execute(query_string)

    fake_db_connection.commit()
    fake_db_connection.close()


def create_table()->None:
    query_str = 'CREATE TABLE IF NOT EXISTS search_app_fakemodel ( ' \
                    'id INTEGER PRIMARY KEY, ' \
                    'first_name VARCHAR(100) NOT NULL, ' \
                    'last_name VARCHAR(100) NOT NULL, ' \
                    'city VARCHAR(100) NOT NULL, ' \
                    'phone_number NCHAR(13) NOT NULL, ' \
                    'national_code NCHAR(10) NOT NULL );'

    execute_query(query_str)


def insert_into_table(data:str)->None:
    query_str = 'INSERT INTO search_app_fakemodel ' \
                    '( first_name, last_name, city, phone_number, national_code ) ' \
                    'VALUES ' + data + ';'
    
    execute_query(query_str)


def joiner(values: Sequence[int]) -> str:
    return "".join(map(str, values))

def add_quotation_mark(value:str)->str:
    return f'"{value}"'


def generate_data(number_of_rows:int)->str:
    f = Faker()
    data=[]

    for _ in range(number_of_rows):
        phone_number = f.random_choices(elements=range(10), length=10)
        national_code = f.random_choices(elements=range(10), length=10)
        data.append(
            [
                add_quotation_mark(f.first_name()),
                add_quotation_mark(f.last_name()),
                add_quotation_mark(f.city()),
                add_quotation_mark("+98" + joiner(phone_number)),
                add_quotation_mark(joiner(national_code)),
            ]
        )

    return '( ' + ' ), ( '.join(', '.join(i) for i in data) + ' )'


def main()->None:
    # create_table()
    data = generate_data(100)
    insert_into_table(data)

if __name__=='__main__':
    main()