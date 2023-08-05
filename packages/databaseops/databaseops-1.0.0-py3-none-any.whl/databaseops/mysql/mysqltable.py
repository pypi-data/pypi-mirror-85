# coding=utf-8
"""
This file is for mysql database connection for user to use database operations as dataframe operations
"""

import pandas
import sqlalchemy
import pymysql.connections
import warnings
from .mysqldatabase import MySQLDataBase


class MySQLTable(MySQLDataBase):
    
    def __init__(self, host: str, user: str, password: str, db_name: str, table_name: str) -> None:
        """
        The object instance of this class will able to perform multiple operations
        on database table like read, filter, sort, remove_duplicates, update etc.
        :param host: Host name of MySQL database.
        :param user: User name of MySQL database.
        :param password: Password for above user name of MySQL database.
        :param db_name: Any MySQL database name from MySQL database.
        :param table_name: Table name from above MySQL database.
        """
        if not hasattr(self, "host") or not hasattr(self, "user") or not hasattr(self, "password") or not hasattr(
                self, "db_name"):
            MySQLDataBase.__init__(self, host, user, password, db_name)
        self.table_name = table_name
        self.__sqlalchemy()
    
    @staticmethod
    def __update_insertion_method(meta: sqlalchemy.MetaData):
        """
        This is privet method. Created for internal used only.
        :param meta: This is the metadata for MySQL database table.
        :return: It returns the method which will be used into update_table.
        """
        
        def method(table, conn, keys, data_iter):
            sql_table = sqlalchemy.Table(table.name, meta, autoload=True)
            insert_stmt = sqlalchemy.dialects.mysql.insert(sql_table).values(
                [dict(zip(keys, data)) for data in data_iter])
            upsert_stmt = insert_stmt.on_duplicate_key_update({x.name: x for x in insert_stmt.inserted})
            conn.execute(upsert_stmt)
        
        return method
    
    def __sqlalchemy(self) -> None:
        """
        This is privet method. Created for internal used only.
        :return: None, But create sqlalchemy_engine.connect inside object instance.
        """
        self.sqlalchemy_engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}", isolation_level="AUTOCOMMIT")
        self.conn = self.sqlalchemy_engine.connect()
    
    def populate_table(self, dataframe: pandas.DataFrame, if_exists: str = 'append') -> None:
        """
        This method add dataframe data to MySQL table.
        :param dataframe: This is pandas.DataFrame which need to added to table.
        :param if_exists: This parameter will decide what to do if table name
        table_name already exists. Options are 'fail', 'replace' and 'append'.
        **Note:** This parameter is about table, Don't confuse it about data inside table.
        :return: None.
        """
        dataframe.to_sql(name=self.table_name, con=self.sqlalchemy_engine, if_exists=if_exists, method=None)
    
    def update_table(self, dataframe: pandas.DataFrame, if_exists: str = 'append') -> None:
        """
        This method will replace data in table if it already exist based upon primary
        key of table.
        :param dataframe: This is pandas.DataFrame which need to added to table.
        :param if_exists: This parameter will decide what to do if table name
        table_name already exists. Options are 'fail', 'replace' and 'append'.
        **Note:** This parameter is about table, Don't confuse it about data inside table.
        :return: None.
        """
        with self.conn.begin():
            meta = sqlalchemy.MetaData(self.conn)
        dataframe.to_sql(name=self.table_name, con=self.sqlalchemy_engine, if_exists=if_exists,
                         method=self.__update_insertion_method(meta))
    
    def get_data_type(self) -> dict:
        """
        This method will give you column name and there data type for entire table.
        :return: dictionary with column name as key and data type as value.
        """
        self.my_cursor.execute(f"Show fields from {self.table_name}")
        return {i[0]: i[1] for i in self.my_cursor}
    
    def remove_duplicates(self, list_of_columns: list) -> None:
        """
        This method will delete duplicates rows from table based upon give list
        of columns. Be caution, as it will directly affect the source table with
        no way of going back.
        :param list_of_columns: list of columns names which should be used for
        removing duplicate values.
        :return: None.
        """
        warnings.warn(f"Removing duplicate entries from columns {','.join(list_of_columns)}", stacklevel=2)
        for col in list_of_columns:
            self.my_cursor.execute(f"CREATE TABLE copy_of_source_{self.table_name} "
                                   f"SELECT * FROM {self.table_name} GROUP BY({col})")
            self.my_cursor.execute(f"DROP TABLE {self.table_name}")
            self.my_cursor.execute(f"ALTER TABLE copy_of_source_{self.table_name} RENAME TO {self.table_name}")
    
    def set_primary_key(self, column_name: str or list, remove_duplicates=True) -> None:
        """
        This method will set "column_name" as primary key for table. caution: By
        default it remove duplicate value for "column_name".
        :param column_name: If str, then it will set as primary key. If list, then
        composite primary key will get created.
        :param remove_duplicates: Either you want delete duplicate value for given
        columns or not. Pass this as False if you don't to remove duplicate on given
        columns, But it will raise exception and primary key will not be set. As
        primary key need to have unique values.
        """
        if isinstance(column_name, str):
            column_name = [column_name]
        self.primary_key_columns = ','.join(column_name)
        if remove_duplicates:
            self.remove_duplicates(column_name)
        database_dtype = self.get_data_type()
        columns = [f'{i}(255)' if 'text' in database_dtype[i] else i for i in column_name]
        try:
            self.my_cursor.execute(f"ALTER TABLE {self.table_name} ADD PRIMARY KEY ({','.join(columns)})")
        except pymysql.err.IntegrityError:
            raise UserWarning(f"Duplicate entries in column {','.join(columns)}, "
                              f"remove_duplicates attribute should be true in case of duplicates")
    
    def set_unique_keys(self, column_name: str or list, remove_duplicates=True) -> None:
        """
        This method will set columns to contain only unique values.
        :param column_name: Column names of database table.
        :param remove_duplicates: Either you want delete duplicate value for given
        columns or not. Pass this as False, if you don't to remove duplicate on given
        columns, But it will raise exception.
        """
        if isinstance(column_name, str):
            column_name = [column_name]
        self.unique_column = ','.join(column_name)
        if remove_duplicates:
            self.remove_duplicates(column_name)
        database_dtype = self.get_data_type()
        columns = [f'{i}(255)' if 'text' in database_dtype[i] else i for i in column_name]
        try:
            self.my_cursor.execute(f"ALTER TABLE {self.table_name} ADD unique ({','.join(columns)})")
        except pymysql.err.IntegrityError:
            raise UserWarning(f"Duplicate entries in column {','.join(columns)},"
                              f" remove_duplicates attribute should be true in case of duplicates")
    
    def sort_table(self, column: str or dict, order="ascending") -> None:
        """
        This method will perform sort operation on source database table.
        :param column: Base on this sorting operation will be performed.
        :param order: Order of sorting, Which can "ascending" or "descending"
        :return: None
        """
        if isinstance(column, str):
            query = f"SELECT * FROM {self.table_name} ORDER BY {column} {order}"
        elif isinstance(column, dict):
            query = f"SELECT * FROM {self.table_name} ORDER BY "
            col_and_order = [[col, c_ord] for col, c_ord in column.items()]
            col_and_order_str = " ,"
            for i in col_and_order:
                col_and_order_str = col_and_order_str.join(i)
            query = query + col_and_order_str
        self.my_cursor.execute(query=query)
    
    def table_filter(self, where: list, select: str or list = None,
                     limit: int = None, chunksize: int = None) -> pandas.DataFrame:
        """
        If you want read filtered table use this method.
        :param where: list of conditions in string format. Ex: ["column_Name = value"]
         OR ["column_Name = Value and  column_Name > Value"] OR
         ["column_Name = Value OR column_Name > Value"]
        :param select: Will only return data for these columns. If None, will
        return complete data
        :param limit: Number of rows
        :param chunksize: Number of rows in one iteration.
        :return: pandas.DataFrame if chunksize is None else iterable object.
        """
        if select:
            if isinstance(select, list):
                query = "SELECT " + " ,".join(select)
            elif isinstance(select, str):
                query = "SELECT " + select
        else:
            query = "SELECT *"
        query = query + f" FROM {self.table_name}" + " where " + " ,".join(where)
        if limit:
            query = query + f" LIMIT {limit}"
        return pandas.read_sql_query(sql=query, con=self.sqlalchemy_engine, chunksize=chunksize)
    
    def read_table(self, chunksize: int = None):
        """
        This method will read table as pandas.DataFrame if chunksize is not given else
        it will return object which can be iterated in for loop every loop will
        given pandas.DataFrame of chunksize.
        :param chunksize: number of row you want read at one time.
        :return: pandas.DataFrame or Iterable object which will give pandas.DataFrame
        """
        return pandas.read_sql_table(table_name=self.table_name, con=self.sqlalchemy_engine, chunksize=chunksize)
