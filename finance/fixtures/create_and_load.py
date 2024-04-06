import calendar
import json
from datetime import datetime
from faker import Faker
from django.contrib.auth.models import User
from finance.models import Currency


def create_fake_json() -> str:
    """
    Create a fixture with fake data in JSON format
    Start with 1 January 2023 and creates IO data up to today.
    Creates between 25 and 50 outcomes and between 2 and 5 incomes
    """

    if len(User.objects.all()) == 0:
        User.objects.create()
    if len(Currency.objects.all()) == 0:
        Currency.objects.create()

    fake = Faker()
    Faker.seed(0)
    this_year = datetime.today().year
    this_month = datetime.today().month
    start_year = 2023
    start_month = 1
    json_list = []

    def create_outcomes_incomes(min_qty, max_qty, is_out, min_int, max_int):
        max_days = calendar.monthrange(start_year, start_month)[1]
        for _ in range(fake.random_int(min=min_qty, max=max_qty)):
            str_date = f'{start_year}-{start_month:02d}-{fake.random_int(min=1, max=max_days)}'
            json_list.append({
                'model': 'finance.oneio',
                "fields": {
                    "is_outcome": is_out,
                    "title": fake.sentence(),
                    "value": fake.random_int(min=min_int, max=max_int),
                    "date": str_date,
                    "owner": 1,
                    "currency": 1,
                    "future": is_out,
                    "cash_tag": None,
                    "company": None,
                    "notes": fake.paragraph(nb_sentences=5),
                    "creation_date": f"{str_date}T00:00:00Z",
                    "last_modification": f"{str_date}T00:00:00Z"
                }
            })

    while True:
        # Expense
        create_outcomes_incomes(25, 50, True, 1, 1000)
        # Income
        create_outcomes_incomes(2, 5, False, 500, 5000)

        start_month += 1
        if start_month > 12:
            start_year += 1
            start_month = 1

        if start_year == this_year and start_month == this_month + 1:
            break
        print(f"Created: {start_year}-{start_month}")

    return json.dumps(json_list, indent=2)