from datetime import datetime

from api.data import BaseQuery


class TweetsQuery(BaseQuery):
    TABLE_NAME = 'tweets'
    def __init__(self, db_instance):
        super().__init__(db_instance, self.TABLE_NAME)

    def get_last_date(self):
        query = f'''
        SELECT
          *
        FROM
          {self.TABLE_NAME}
        ORDER BY
          tweet_date
        LIMIT
          1
        '''

        self.execute(query)
        rows = self.fetch()

        return rows[0]['created_at'] if rows else None

    def save_tweet(self, user_id, tweet_text, tweet_date, place):
        data = {
            'user_id': user_id,
            'tweet_text': tweet_text,
            'tweet_date': self._datetime_from_str(tweet_date),
            'place': place,
        }

        try:
            self.save_row(data)
        except UnicodeEncodeError:
            self._conn.rollback()
            print('unable to encode tweet')

    def get_tweets(self, from_date=None, to_date=None):
        if from_date and to_date:
            where = '''
            WHERE
              tweet_date >= %(from_date)s
              AND
              tweet_date <= %(to_date)s
            '''
            data = {'from_date': from_date,
                    'to_date': to_date}
        elif from_date and not to_date:
            where = '''
            WHERE
              tweet_date >= %(from_date)s
            '''
            data = {'from_date': from_date}
        elif to_date and not from_date:
            where = '''
            WHERE
              tweet_date <= %(to_date)s
            '''
            data = {'to_date': to_date}
        else:
            where = ''
            data = None
        query = f'''
        SELECT
          *
        FROM 
          {self.TABLE_NAME}
        {where}
        ORDER BY
          tweet_date ASC
        '''

        self.execute(self.prepare_query(query, data))
        return self.fetch()

