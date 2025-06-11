#  bluefaker_factory

A modular, schema-driven synthetic data generator built with [Faker](https://faker.readthedocs.io/en/master/) for simulating rich, realistic datasets. Ideal for machine learning testing, analytics development, data engineering demos, and pipeline validation.

---

## Features

- YAML-based schema definitions for customizable data types
- Parallel data generation for high performance
- Output in CSV, Parquet, or JSON
- Built-in support for domains like churn, fraud, transactions, and support tickets
- Includes SQL examples and Examples use DuckDB for quick integration
- Modular plugins for injecting custom domain specific business logic

---

## Directory Structure

```
bluefaker_factory/
├── bluefaker.py              # Main data generation engine
├── data/
│   ├── raw/                  # Generated datasets
│   └── database/             # Optional local DuckDB files
├── examples/
│   └── sql_fraud/            # Sample SQL for analysis
|-- logic_modules/            # Domain-specific business logic plugins
├── schemas/                  # YAML schemas (fraud, churn, etc.)
├── scripts/                  # Shell wrappers for schema-specific generation
├── requirements.txt          # Python dependencies
└── README.md                 # You're reading it
````

---

## 
Usage

### Install dependencies
```bash
pip install -r requirements.txt
````

### Generate data with a YAML schema

```bash
python bluefaker.py \
  --schema schemas/YOUR_SCHEMA.yaml \
  --records 10000 \
  --format parquet \
  --file data/raw/YOUR_DATA_NAME
```

You can also append data to an existing file using `--append`.

If you already have a file with data that matches your schema, you can use `--append` to add more rows to it. For example, the command below will add 100,000 additional rows:

```bash
python bluefaker.py \
  --schema schemas/YOUR_SCHEMA.yaml \
  --records 100000 \
  --format parquet \
  --file data/raw/YOUR_DATA_NAME \
  --append
```

---

## Example: Generating 100,000 Fraud Records

Here’s an example of generating 100K fraud records using a shell script wrapper:

**`scripts/create_fake_fraud_data.sh`**
```bash
python bluefaker.py --schema schemas/fraud_schema.yaml \
                       --records 100000 \
                       --format parquet \
                       --file data/raw/fraud_data01
```
This will create a parquet file called `fraud_data01.parquet` with 100,000 rows of fake synthetic fraud data. 

### Run an example script

```bash
bash scripts/create_fake_fraud_data.sh
```
Example:
```bash
(.venv) $ time ./scripts/create_fake_fraud_data.sh

Generating Fake Data with '100000' records....

100%|███████████████████████████████████████████████████| 100000/100000 [00:25<00:00, 3998.42it/s]

Sample Data:
+--------------------------------------+----------------+---------------------------+------------+-----+-------------+--------------+---------------+-----------+--------------------+----------------------+------------------------------------------------------------------+-------------+------------+---------+--------------+--------------+
|                  ID                  |      Name      |           Email           |   Gender   | Age |   Country   | Credit_Score | Annual_Income | Card_Type | Transaction_Amount | Transaction_Location |                              Device                              | Time_Of_Day | Fraudulent | Churned | VIP_Customer | At_Risk_Flag |
+--------------------------------------+----------------+---------------------------+------------+-----+-------------+--------------+---------------+-----------+--------------------+----------------------+------------------------------------------------------------------+-------------+------------+---------+--------------+--------------+
| 36dfdc6a-dbb6-4160-8e3b-45e7aff187bc |  Erin Finley   |   erin.finley@clark.info  | Non-binary |  52 |   Nigeria   |     565      |     163199    |     b     |       546.83       |      Webershire      | Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.01; Trident/4.1) |   06:28:36  |    True    |   True  |    False     |    False     |
| 1de49109-29a2-4021-a66d-24160d58d10f | Kristen Austin | kristen.austin@garcia.com | Non-binary |  57 | Switzerland |     382      |     139646    |     c     |       875.08       | West Matthewborough  | Opera/9.59.(Windows NT 5.01; sl-SI) Presto/2.9.181 Version/12.00 |   02:48:07  |   False    |   True  |    False     |    False     |
| 1a2a894b-c7d6-4929-bcb8-eb419845f96b |  Andrew Potts  |  andrew.potts@rowland.com | Non-binary |  60 |    Angola   |     424      |     39213     |     b     |       542.5        |   North Jacobville   | Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.2; Trident/4.0)  |   20:58:17  |   False    |   True  |    False     |    False     |
+--------------------------------------+----------------+---------------------------+------------+-----+-------------+--------------+---------------+-----------+--------------------+----------------------+------------------------------------------------------------------+-------------+------------+---------+--------------+--------------+

Created file: ../data/raw/fraud_data01.parquet  
Number of rows added: 100000
```
This create the file with 100k rows in 25 seconds. 

---

## Available Schemas

| Schema                       | Purpose                                          |
| ---------------------------- | ------------------------------------------------ |
| `fraud_schema.yaml`          | Simulates transactions with fraud logic          |
| `churn_schema.yaml`          | Tracks engagement and churn behaviors            |
| `transaction_schema.yaml`    | E-commerce or financial transaction data         |
| `support_ticket_schema.yaml` | Customer support and escalation flows            |
| `ml_schema.yml`              | General-purpose features for ML training/testing |

> You can create your own by copying an existing one and modifying columns/types.

## Extendable Rule-Based Logic (Plugin)

To simulate realistic behavioral signals in your synthetic data like **fraud**, **churn**, or **VIP customer patterns** — `bluefaker_factory` supports **pluggable domain logic modules**.

Each YAML schema can declare one or more `domains`, and the generator will dynamically apply the corresponding rule logic from the `logic_modules/` folder.

### Example Schema Snippet

```yaml
domains:
  - fraud
  - churn

schema:
  - column: ID
    dtype: uuid4
  - column: Name
    dtype: name
  - column: Email
    dtype: email
  ......

```

This will automatically load and apply:

* `logic_modules/fraud.py`
* `logic_modules/churn.py`

---

### How It Works

Each logic module (e.g. `fraud.py`, `churn.py`, etc.) must define an `apply(row)` function that adds fields, flags, or modifications to the generated row.

Example logic (`logic_modules/churn.py`):

```python
def apply(row):
    if row.get("Subscription_Level") == "Free" and row.get("Num_Sessions", 0) < 10:
        row["Churned"] = True
    return row
```

The main generator uses Python's `importlib` to load these dynamically based on the `domains` listed in the schema.

---

### Add Your Own Logic

1. Create a new file in `logic_modules/`, like `vip.py`
2. Define an `apply(row)` function inside it
3. Reference it in your schema YAML:

```yaml
domains:
  - vip
```

That’s it, your logic is now applied automatically during data generation.

---

## Analyze the Data

Use DuckDB, pandas, or SQL to analyze:

```sql
SELECT Country, COUNT(*) AS total, AVG(Transaction_Amount)
FROM read_parquet('data/raw/fraud_data.parquet')
GROUP BY Country
ORDER BY total DESC
LIMIT 10;
```

Or use included SQL in `examples/sql_fraud/`.

---

## Quickstart with DuckDB for quick exploration 🦆

DuckDB is a lightweight SQL engine optimized for analytics. You can explore your generated datasets without any setup.

It is great for many things but a few:

* **Data scientists** exploring outputs interactively
* **Engineers** validating fake data pipelines
* **Analysts** prototyping queries without a full database setup

### Install DuckDB Python Libraries

```bash
pip install duckdb
```

### To Get the CLI (duckdb shell command)
You need to install it separately via one of the following:

🔹 macOS (with Homebrew)
```bash
brew install duckdb
```
🔹 Linux (Debian/Ubuntu)
```bash
sudo apt install duckdb
```

🔹 Windows
Use the DuckDB Windows installer or extract the CLI binary manually from GitHub releases.

Or download the binary from the official site:
👉 https://duckdb.org/docs/installation/

### Run SQL directly from the CLI

#### In memmory:
```bash
duckdb
````

#### Or to persist the data on disk:

```bash

duckdb data/database/blue_duck.db

```

Then query a Parquet file:

```sql
SELECT * FROM 'data/raw/fraud_data.parquet' LIMIT 5;

SELECT
  Country,
  COUNT(*) AS total,
  SUM(CASE WHEN Fraudulent THEN 1 ELSE 0 END) AS fraud_count
FROM read_parquet('data/raw/fraud_data.parquet')
GROUP BY Country
ORDER BY fraud_count DESC
LIMIT 10;
```

To create a native table from a file:
```sql
CREATE TABLE fraud_data AS 
SELECT * FROM read_parquet('fraud_data01.parquet');
```
To Quit:
`.q`

### Use DuckDB in Python

```python
import duckdb

df = duckdb.query("SELECT * FROM 'data/raw/fraud_data.parquet'").to_df()
print(df.head())
```

## License

MIT

---

## Contributing

Ideas? Bug fixes? PRs are welcome!

---

```

---

```




