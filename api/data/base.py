from datetime import datetime

class BaseQuery(object):
    def __init__(self, db_instance, table_name=None):

        self._conn = db_instance
        self._cur = self._conn.cursor()
        self.table_name = table_name
        self.schema = self._query_config()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def _query_config(self):
        query = '''
        SELECT
          *
        FROM
          information_schema.columns
        WHERE
          table_name = %(str)s
        ORDER BY
          ordinal_position
        '''

        values = {'str': self.table_name}

        self.execute(self.prepare_query(query, values))
        rows = self._cur.fetchall()

        return [r[3] for r in rows]

    def _datetime_from_str(self, s):
        return datetime.strptime(s, '%a %b %d %H:%M:%S %z %Y')

    def save_row(self, data: dict):
        assert type(data) is dict
        data['created_at'] = datetime.now()

        columns = '(' + ', '.join(data.keys()) + ')'
        values = '(' + ', '.join([f'%({key})s' for key in data.keys()]) + ')'

        query = f'''
        INSERT INTO
          {self.table_name} {columns}
        VALUES
          {values}
        RETURNING
          *;
        '''

        statement = self.prepare_query(query, data)
        self.execute(statement)
        self._conn.commit()
        r = self.fetch()
        return r

    def prepare_query(self, query, values=None):
        return self._cur.mogrify(query, values)

    def execute(self, query):
        self._cur.execute(query)

    def fetch(self):
        rows = self._cur.fetchall()
        return [dict(zip(self.schema, row)) for row in rows]
