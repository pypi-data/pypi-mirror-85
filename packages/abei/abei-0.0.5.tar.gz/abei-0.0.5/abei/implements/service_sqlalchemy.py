from abei.interfaces import (
    IStorage,
    IService,
    service_entry as _
)
from .service_basic import ServiceBasic


class Service(ServiceBasic, IService):

    @classmethod
    def get_dependencies(cls):
        return ['SQLAlchemy==1.3.8']

    def __init__(self, service_site, **kwargs):
        from sqlalchemy import create_engine
        service = service_site.get_service(_(IStorage))
        sa_connection = service.get_value('sqlalchemy:connection')
        sa_echo = service.get_value('sqlalchemy:debug')
        sa_pool_size = service.get_value('sqlalchemy:pool_size')
        sa_pool_recycle = service.get_value('sqlalchemy:pool_recycle')
        self.sa_engine = create_engine(
            sa_connection
            or "mysql://root:2v0eps4o@127.0.0.1:3306/mb?charset=utf8",
            echo=sa_echo or False,
            pool_size=sa_pool_size or 2,
            pool_recycle=sa_pool_recycle or 3600)
        print("----service sqlalchemy component initialized----")
