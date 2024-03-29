import psycopg2


class DataBase:
    '''
    Class for connecting to a user database
    and operating with it within the current application
    '''
    def __init__(self, DATABASE_URL: str):
        '''
        Environment variable
        For example: postgresql://user:password@localhost:5432/mydb
        '''
        self.database_url = DATABASE_URL

    def _connect_db(self):
        '''
        Connection in database
        '''
        try:
            return psycopg2.connect(self.database_url)

        except ValueError:
            print('Can`t establish connection to database')

    def _close_connect_db(self, connect) -> None:
        '''
        Closing connect to database
        '''
        connect.close()

    def _get_all_fields(self, connect, name_table: str) -> str:
        '''
        Getting all field names from the requested table
        '''
        with connect.cursor() as cursor:
            cursor.execute(f'SELECT * FROM {name_table} LIMIT 0;')
            select_all = ', '.join([
                row[0]
                if row[0] != 'created_at'
                else 'DATE(created_at)'
                for row in cursor.description
            ])
        self._close_connect_db(connect)
        return select_all

    def _add_where(self, clause_where: (str, str)):
        '''
        Creating a conditional part of a query
        '''
        name_field, value = clause_where
        if name_field:
            where_request = f' WHERE {name_field}=(%s)'
            value = (value, )
            return (where_request, value)

        return ('', None)

    def _add_order(self, name_field: str) -> str:
        '''
        Creating a sortional part of a query
        '''
        return f' ORDER BY {name_field} DESC' if name_field else ''

    def get_data_table(
        self,
        name_table: str,
        clause_select='',
        clause_where: (str, str) = ('', ''),
        clause_order: str = ''
    ):
        '''
        Retrieving data from database as per query
        '''
        if not isinstance(clause_select, str):
            clause_select = ', '.join(
                [name_field for name_field in clause_select]
            )

        if not clause_select:
            clause_select = self._get_all_fields(
                self._connect_db(),
                name_table
            )

        where_request, request_params = self._add_where(clause_where)
        order_request = self._add_order(clause_order)

        request_ = f'SELECT {clause_select}' \
                   f' FROM {name_table}' \
                   f'{where_request}{order_request};'

        connect = self._connect_db()
        with connect.cursor() as cursor:
            cursor.execute(request_, request_params)
            result = cursor.fetchall()
        self._close_connect_db(connect)

        return result

    def change_table(self, name_table: str, name_fields, data_fields):
        '''
        Changing database as per query
        '''
        req_values = ', '.join('%s' for i in name_fields)
        name_fields = ', '.join(name for name in name_fields)

        request_ = f'INSERT INTO {name_table} ({name_fields})' \
                   f' VALUES ({req_values});'

        connect = self._connect_db()
        with connect.cursor() as cursor:
            cursor.execute(request_, data_fields)
        connect.commit()
        self._close_connect_db(connect)

    def left_join_urls_and_url_cheks(self):
        '''
        Joiing tables for more information
        '''
        request_ = '''
            SELECT urls.id AS id,
                urls.name AS name,
                DATE(max(url_checks.created_at)) AS last_checks,
                url_checks.status_code AS status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id=url_checks.url_id
            GROUP BY urls.id, url_checks.status_code
            ORDER BY urls.id DESC;'''

        connect = self._connect_db()
        with connect.cursor() as cursor:
            cursor.execute(request_)
            result = cursor.fetchall()
        self._close_connect_db(connect)

        return result
