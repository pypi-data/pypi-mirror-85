class Data(dict):
    """Actually a superset class of python dictionaries, which also supports accessing of its keys using . syntax.

    UNUSED FOR THE MOMENT.

    Extra Attributes
    ----------------

    created_at : datetime.datetime
        The time this data was created in UTC.

    """

    def __setattr__(self, key, value):
        self[key] = value

    def __getattribute__(self, item):
        try:
            data = self[str(item)]
        except KeyError:
            raise AttributeError
        else:
            try:
                return int(data)
            except ValueError:
                return data
