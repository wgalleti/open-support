import fdb


class FirebirdConnector:
    CHARSET = 'utf-8'

    def _load_string(self, connection):
        """
        Sample connection connection = "firebird://sysdba:masterkey@localhost/c:\dados\hifuzion.fdb"
        :param connection:
        :return:
        """

        _, connection = connection.split('://')
        credentials, connection = connection.split('@')
        self.user, self.password = credentials.split(':')
        if connection.find('//') != -1:
            self.host, self.database = connection.split('//')
            self.database = '/' + self.database
        else:
            self.host, self.database = connection.split('/')

        self.port = 3050

        if self.host.find(':'):
            self.host, self.port = self.host.split(':')
            self.port = int(self.port)

    def __init__(self, **kwargs):
        self._load_string(kwargs.get('connection', None))
        self.connection: fdb.connect = None
        self.str_connection = {}
        self.columns = []
        self.connect()

    def get_str_connection_line(self):
        return ''.join([f'{i[0].title()} {i[1]}, ' for i in self.str_connection.items()])[:-2]

    def connect(self):
        """
        Connect with database
        """
        self.str_connection = dict(host=self.host,
                                   database=self.database,
                                   user=self.user,
                                   port=self.port,
                                   password=self.password,
                                   charset=self.CHARSET)
        self.connection = fdb.connect(**self.str_connection)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def next(self, generator: str) -> int:
        sql = '''select gen_id(%GEN%, 1) as id from rdb$database'''.replace('%GEN%', generator.upper())

        row = self.get(sql)

        if len(row) == 0:
            raise Exception('Cannot locate generator')

        return row[0].get('id', 0)

    def insert_retunig_id(self, sql, params=None):
        sql += ' returning id'
        row = self.get(sql, params)

        if len(row) == 0:
            raise Exception('Cannot find retuning command')

        return row[0].get('id', 0)

    def select_all(self, table):
        """
        Return list of data with base SELECT statement
        """
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT * FROM {table}', None)
        self.columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(self.columns, row)) for row in cursor.fetchall()]

    def get(self, query, params=None):
        """
        Return list of data with base SELECT statement
        """
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(self.columns, row)) for row in cursor.fetchall()]

    def execute(self, comand, params=None, auto_commit=True):
        """
        Run SQL command
        """
        cursor = self.connection.cursor()
        cursor.execute(comand, params)

        if auto_commit:
            self.connection.commit()

# Doc
# https://fdb.readthedocs.io/en/v2.0/getting-started.html#quick-start-guide
