from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.orm.exc import NoResultFound
from fyp.server.exc import NotFound

class Assistant:
    @classmethod
    def getBy(model, session, **kwargs):

        where = None
        for attr, value in kwargs.iteritems():
            try:
                comp = model.__dict__[attr] == value
            except Exception, e:
                raise AttributeError("Attribute '%s' not found on model '%s'." % (attr, model.__name__))                

            where = comp if not where else where & comp

        try:
            return session.query(model).filter(where).one()
        except NoResultFound:
            raise NotFound(model.__name__)

    def dump(self, schema):
        return schema.dump({ prop.key: getattr(self, prop.key) for prop in class_mapper(self.__class__).iterate_properties 
            if isinstance(prop, ColumnProperty) }).data
