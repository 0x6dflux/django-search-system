from typing import Sequence

from faker import Faker

# from config.models import FakeModel

f = Faker()
data: list = []


def joiner(values: Sequence[int]) -> str:
    return "".join(map(str, values))


for _ in range(10):
    phone_number = f.random_choices(elements=range(10), length=10)
    national_code = f.random_choices(elements=range(10), length=10)
    data.append(
        [
            f.first_name,
            f.last_name,
            f.city,
            "+98" + joiner(phone_number),
            joiner(national_code),
        ]
    )

    print(data)
