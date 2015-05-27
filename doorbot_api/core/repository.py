# -*- coding: utf-8 -*-


class Repository(object):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None

    def __init__(self, session):
        self._session = session
        self.account_id = 0

    def set_session(self, session):
        self._session = session

    def set_account_scope(self, account_id):
        self.account_id = account_id

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not
        the expected type.

        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def save(self, model, immediate=True):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        self._isinstance(model)
        self._session.add(model)

        if immediate:
            self._session.commit()

        return model

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        print(self.__model__)
        return self._session.query(self.__model__).all()

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self._session.query(self.__model__).get(id)

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self._session.query(self.__model__).filter_by(**kwargs)

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).first()

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.save(self.new(**kwargs))

    def delete(self, model, immediate=True):
        """Deletes the specified instance

        :param model: the model instance to delete
        :param immediate: Immediately delete the instance.
        """
        self._isinstance(model)
        self._session.delete(model)

        if immediate:
            self._session.commit()
