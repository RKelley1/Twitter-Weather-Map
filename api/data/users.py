from psycopg2 import IntegrityError

from api.data import BaseQuery

class UsersQuery(BaseQuery):
    TABLE_NAME = 'users'
    def __init__(self, db_instance):
        super().__init__(db_instance, self.TABLE_NAME)

    def save_user(self, twitter_id, screen_name, user_date):

        data = {
            'twitter_id': twitter_id,
            'screen_name': screen_name,
            'user_date': self._datetime_from_str(user_date),
        }

        try:
            row = self.save_row(data)[0]
        except IntegrityError:
            self._conn.rollback()
            row = self.get_user_by_twitter_id(twitter_id)

        return row

    def get_user_by_twitter_id(self, twitter_id):
        query = f'''
        SELECT
          *
        FROM
          {self.table_name}
        WHERE
          twitter_id = %(twitter_id)s
        LIMIT
          1;
        '''

        self.execute(self.prepare_query(query, {'twitter_id': twitter_id}))
        rows = self.fetch()
        return rows[0] if len(rows) >= 1 else None
