import hug

from api.bootstrap import Bootstrap
from api.types import ResourceTypes
from api.config import config
from api.resources import (
    BocaResource,
    TwitterResource,
)

api_root = __name__
Bootstrap.configure(api_root, {
    Bootstrap.RESOURCES: {
        ResourceTypes.BOCA: BocaResource,
        ResourceTypes.TWITTER: TwitterResource,
    }
})


