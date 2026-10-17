import json
import sys
from faker import Faker

def generate_random_users(count=5, locale="en_IN"):
    fake = Faker(locale)
    users = []
    for _ in range(count):
        profile = fake.simple_profile()
        user_record = {
            "name": fake.name(),
            "username": profile.get("username"),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "job": fake.job(),
            "company": fake.company(),
            "address": fake.address().replace("\n", ", "),
            "birthdate": str(profile.get("birthdate")),
            "credit_card_type": fake.credit_card_provider(),
            "ipv4": fake.ipv4()
        }
        users.append(user_record)
    return users

def display_users(users):
    print("=" * 65)
    print(f"GENERATED RANDOM USERS (Total: {len(users)})")
    print("=" * 65)
    for idx, user in enumerate(users, 1):
        print(f"[{idx}] {user['name']} (@{user['username']})")
        print(f"    Email       : {user['email']}")
        print(f"    Phone       : {user['phone_number']}")
        print(f"    Company     : {user['company']}")
        print(f"    Occupation  : {user['job']}")
        print(f"    Address     : {user['address']}")
        print(f"    Birthdate   : {user['birthdate']}")
        print(f"    IP Address  : {user['ipv4']}")
        print("-" * 65)

def main():
    count = 3
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass

    users = generate_random_users(count)
    display_users(users)

    if "--json" in sys.argv:
        print("\nJSON Output:")
        print(json.dumps(users, indent=2))

if __name__ == "__main__":
    main()
