from api.data.base import BaseQuery

class TestQuery(BaseQuery):
    TABLE_NAME = 'test_table'
    def __init__(self, db_instance):
         super().__init__(db_instance, self.TABLE_NAME)

    def test_query(self):
        query = '''
        SELECT
         *
        FROM
          test_table;
        '''
 
        self.execute(query)
        return self.fetch()
