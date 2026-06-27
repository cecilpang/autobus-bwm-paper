import sqlite3
import random
from config import DB_PATH, DB_DIR
import os

random.seed(12345)

ddl = """
    DROP TABLE IF EXISTS consumer;
    CREATE TABLE consumer (
        consumer_id INTEGER PRIMARY KEY,
        consumer_name TEXT,
        city TEXT
    );
    DROP TABLE IF EXISTS profile_attribute;
    CREATE TABLE profile_attribute (
        consumer_id INTEGER,
        attribute_name TEXT,
        attribute_value TEXT,
        PRIMARY KEY(consumer_id, attribute_name),
        FOREIGN KEY(consumer_id) REFERENCES consumer(consumer_id)
    );
    DROP TABLE IF EXISTS product;
    CREATE TABLE product (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        standard_rate NUMERIC  -- 10, 15, or 20
    );
    DROP TABLE IF EXISTS subscription;
    CREATE TABLE subscription (
        subscription_id INTEGER PRIMARY KEY,
        consumer_id INTEGER,
        status TEXT, -- Active/Inactive 
        subscription_rate NUMERIC,  -- 1 to 20, and <= product.standard_rate
        product_id INTEGER,
        risk_level INTEGER, -- 1 to 5
        FOREIGN KEY(consumer_id) REFERENCES consumer(consumer_id),
        FOREIGN KEY(product_id) REFERENCES product(product_id)
    );
    DROP TABLE IF EXISTS savable_churn;
    CREATE TABLE savable_churn 
    (
        subscription_id INTEGER PRIMARY KEY,
        consumer_id INTEGER
    );
    DROP TABLE IF EXISTS median_household_income;
    CREATE TABLE median_household_income 
    (
        city TEXT PRIMARY KEY,
        median_household_income INTEGER
    );
    DROP TABLE IF EXISTS target_subscription;
    CREATE TABLE target_subscription (
        subscription_id INTEGER PRIMARY KEY,
        status TEXT,
        product_name TEXT, -- Active/Inactive 
        risk_level NUMERIC,  -- 1 to 20, and <= product.standard_rate
        subscription_rate INTEGER,
        household_income INTEGER, -- 1 to 5
        median_household_income INTEGER
    );
"""

def create_tables(conn):
    conn.executescript(ddl)
    conn.commit()

def insert_products(conn):
    """
    Insert 5 products with standard_rate in {10, 15, 20}.
    """
    products = [
        ("Basic Plan", 10),
        ("Standard Plan", 15),
        ("Premium Plan", 20),
        ("Family Plan", 20),
        ("Student Plan", 5),
    ]
    conn.executemany(
        "INSERT INTO product (product_name, standard_rate) VALUES (?, ?)",
        products,
    )
    conn.commit()

def insert_consumers(conn, n_consumers=10000):
    """
    Insert n_consumers into consumer table.
    """
    cities = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
        "Austin", "Jacksonville", "San Francisco", "Columbus", "Charlotte",
        "Seattle", "Denver", "Washington", "Boston", "Detroit"
    ]

    consumers = []
    for i in range(1, n_consumers + 1):
        name = f"Consumer {i}"
        city = random.choice(cities)
        consumers.append((name, city))

    conn.executemany(
        "INSERT INTO consumer (consumer_name, city) VALUES (?, ?)",
        consumers,
    )
    conn.commit()

def insert_subscriptions(conn, n_active=500, n_inactive=1000):
    """
    Insert subscriptions with these constraints:
    - Exactly n_active active subscriptions
    - Exactly n_inactive inactive subscriptions
    - A consumer cannot have more than 1 active subscription
    - subscription_rate: 1–20 AND <= product.standard_rate
    - risk_level: 1–5
    """
    cursor = conn.cursor()

    # Get all consumer_ids
    cursor.execute("SELECT consumer_id FROM consumer")
    consumer_ids = [row[0] for row in cursor.fetchall()]

    # Get all products with their standard_rate
    cursor.execute("SELECT product_id, standard_rate FROM product")
    products = cursor.fetchall()  # list of (product_id, standard_rate)

    subscriptions = []

    # --- Active subscriptions: choose n_active DISTINCT consumers ---
    active_consumers = random.sample(consumer_ids, n_active)
    for consumer_id in active_consumers:
        product_id, standard_rate = random.choice(products)
        max_rate = min(20, int(standard_rate))
        subscription_rate = random.randint(1, max_rate)
        risk_level = random.randint(1, 5)
        status = "Active"
        subscriptions.append(
            (consumer_id, status, subscription_rate, product_id, risk_level)
        )

    # --- Inactive subscriptions: can be multiple per consumer, may overlap active set ---
    for _ in range(n_inactive):
        consumer_id = random.choice(consumer_ids)
        product_id, standard_rate = random.choice(products)
        max_rate = min(20, int(standard_rate))
        subscription_rate = random.randint(1, max_rate)
        risk_level = random.randint(1, 5)
        status = "Inactive"
        subscriptions.append(
            (consumer_id, status, subscription_rate, product_id, risk_level)
        )

    conn.executemany(
        """
        INSERT INTO subscription (consumer_id, status, subscription_rate, product_id, risk_level)
        VALUES (?, ?, ?, ?, ?)
        """,
        subscriptions,
    )
    conn.commit()

def insert_profile_attributes(conn):
    """
    Insert profile attributes with probabilities:
    - Consumers WITH any subscription: 75% chance per attribute
    - Consumers WITHOUT any subscription: 10% chance per attribute

    Attributes:
      - age_group
      - education
      - household_size
      - household_income  (20000 to 300000)
    """
    age_groups = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    educations = ["High School", "Some College", "Bachelor", "Master", "Doctorate"]
    household_sizes = ["1", "2", "3", "4", "5+"]
    # household_income is numeric, but stored as TEXT in attribute_value
    income_min, income_max = 20000, 300000

    cursor = conn.cursor()

    # All consumers
    cursor.execute("SELECT consumer_id FROM consumer")
    consumer_ids = [row[0] for row in cursor.fetchall()]

    # Consumers that have ANY subscription (active or inactive)
    cursor.execute("SELECT DISTINCT consumer_id FROM subscription")
    subscribed_consumers = {row[0] for row in cursor.fetchall()}

    attributes_to_insert = []

    for cid in consumer_ids:
        prob = 0.75 if cid in subscribed_consumers else 0.10

        # age_group
        if random.random() < prob:
            attributes_to_insert.append(
                (cid, "age_group", random.choice(age_groups))
            )

        # education
        if random.random() < prob:
            attributes_to_insert.append(
                (cid, "education", random.choice(educations))
            )

        # household_size
        if random.random() < prob:
            attributes_to_insert.append(
                (cid, "household_size", random.choice(household_sizes))
            )

        # household_income
        if random.random() < prob:
            household_income = random.randint(income_min, income_max)
            attributes_to_insert.append(
                (cid, "household_income", str(household_income))
            )

    if attributes_to_insert:
        conn.executemany(
            """
            INSERT INTO profile_attribute (consumer_id, attribute_name, attribute_value)
            VALUES (?, ?, ?)
            """,
            attributes_to_insert,
        )
        conn.commit()

def get_subscriptions_filtered(
    db_path="subscriptions.sqlite",
    age_groups=("55-64", "65+"),
    educations=("Master", "Doctorate"),
    risk_level=4,
    min_subscription_rate=10,
):
    """
    Get subscriptions where:
      - subscriber age_group is in `age_groups`
      - subscriber education is in `educations`
      - subscription risk_level = `risk_level`
      - subscription_rate >= `min_subscription_rate`

    Returns a list of tuples:
      (subscription_id, consumer_id, consumer_name, city,
       status, subscription_rate, product_name, risk_level,
       age_group, education)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Build dynamic placeholders for IN clauses
    age_placeholders = ",".join("?" for _ in age_groups)
    edu_placeholders = ",".join("?" for _ in educations)

    query = f"""
        SELECT
            s.subscription_id,
            c.consumer_id,
            c.consumer_name,
            c.city,
            s.status,
            s.subscription_rate,
            p.product_name,
            s.risk_level,
            age_attr.attribute_value AS age_group,
            edu_attr.attribute_value AS education
        FROM subscription s
        JOIN consumer c
            ON s.consumer_id = c.consumer_id
        JOIN product p
            ON s.product_id = p.product_id
        JOIN profile_attribute age_attr
            ON age_attr.consumer_id = c.consumer_id
           AND age_attr.attribute_name = 'age_group'
        JOIN profile_attribute edu_attr
            ON edu_attr.consumer_id = c.consumer_id
           AND edu_attr.attribute_name = 'education'
        WHERE age_attr.attribute_value IN ({age_placeholders})
          AND edu_attr.attribute_value IN ({edu_placeholders})
          AND s.risk_level = ?
          AND s.subscription_rate >= ?
    """

    params = list(age_groups) + list(educations) + [risk_level, min_subscription_rate]

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def main():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    create_tables(conn)
    insert_products(conn)
    insert_consumers(conn, n_consumers=10000)
    insert_subscriptions(conn, n_active=500, n_inactive=1000)
    insert_profile_attributes(conn)

    conn.close()
    print(f"Sample data inserted into {DB_PATH}")

if __name__ == "__main__":
    main()
