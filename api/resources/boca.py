import hug

from api.resources import ResourceAbstract
from api.types import ResourceTypes
from api.methods import get_html
from api.data import TestQuery
from api.config import config


class BocaResource(ResourceAbstract):
    def __init__(self, root_path=None):
        super().__init__(root_path)

    def get_type(self):
        return ResourceTypes.BOCA

    @get_html.urls('/boca')
    def get_things(self, request, response):
        q = TestQuery(config.get_db())
        rows = q.test_query()

        headers = ''.join(f'<th>{key}</th>' for key in rows[0].keys())

        data = ''
        for row in rows:
            data += '<tr>'
            for value in row.values():
                data += f'<td>{value}</td>'
            data += '</tr>'

        return f'''
        <html>
            <body>
                <table>
                    <tr>
                        {headers}
                    </tr>
                    {data}
            </body>
        </html>
        '''
