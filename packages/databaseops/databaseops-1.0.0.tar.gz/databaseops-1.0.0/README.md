# DatabaseOps

---

A lightweight and fast database operation module without using queries with the ease of python.

## Table of Contents

- [Install](#install)
- [Dependencies](#Dependencies)
- [Usage](#usage)
- [Contributing](#Contributing)
- [License](#license)
- [Project status](#Project-status)


## Install

``` python
 pip install databaseops
```

**Note:** Above example will always fetch the latest version. To fetch a specific version, use `pip install
 databaseops==Version`
Visit [databseops/history](https://pypi.org/project/databaseops/#history) to see older versions.

## Dependencies
- [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)
- [sqlalchemy](https://www.sqlalchemy.org/)
- [PyMySQL](https://pymysql.readthedocs.io/en/latest/#)

**Note:** You don't need to worry about dependencies as all those will install automatically 
at the installing databaseops. This information is just for your knowledge. 

## Usage

``` python
from databaseops import MySQLTable
my_sql_table = MySQLTable(host="localhost", user="root", password="1234", db_name="Test", table_name="Test_table")
```

Explanation and usage of different methods available to user are as follows
``` python
# Populate Table: Add data frame to database table
my_sql_table.populate_table(dataframe=pandas.DataFrame, if_exists: str = 'append')

# Update Table
my_sql_table.update_table(dataframe=pandas.DataFrame, if_exists: str = 'append')

# Set Primary Key
my_sql_table.set_primary_key(column_name= "single column name" or ["list of column names"],
 remove_duplicates=True) 

# Set Unique Keys
my_sql_table.set_unique_keys(column_name= "single column name" or ["list of column names"],
 remove_duplicates=True)

# Read Table
my_sql_table.read_table(chunksize: int = None)

# Table Filter
my_sql_table.table_filter(where: [list of condition], select= "single column name" or ["list of column names"],
 limit: int = None, chunksize: int = None)

# Remove Duplicates
my_sql_table.remove_duplicates(list_of_columns= ["list of column names"])


# Sort Table
my_sql_table.sort_table(column: str or dict, order="ascending" or "descending")

# Get Data Type
my_sql_table.get_data_type()
```

## Roadmap

Plan for future releases is to add multi-table join and other query to MySqlOps class.
After that plan is add support to multiple databases like [redis](https://redis.io/), 
[mongoDB](https://www.mongodb.com/what-is-mongodb)


## Contributing
Pull requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.

## License

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

Released 2020 by [Ankush Bhise](https://github.com/AnkushBhise)

## Project status
This project is in development mode, not completely developed yet.
It will developed at slower speed.