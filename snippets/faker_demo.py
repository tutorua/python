from faker import Faker

faker = Faker()
for _ in range(6):
    print(f'name: {faker.name()}')
    print(f'address: {faker.address()}')
    print(f'url: {faker.url()}')
    print(f'date: {faker.date()}')
    print(f'company: {faker.company()}')
    print(f'text: {faker.text()}')
    print()


