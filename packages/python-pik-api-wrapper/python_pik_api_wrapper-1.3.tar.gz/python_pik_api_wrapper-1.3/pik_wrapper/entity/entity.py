class Entity:
    def __init__(self, id_or_dict):
        id = id_or_dict
        if isinstance(id_or_dict, dict):
            id = id_or_dict.get('id')
        if not isinstance(id, str):
            raise ValueError
        self.id = id

    def __repr__(self):
        str_list = []
        for item in self.__dict__:
            if type(getattr(self, item)) is list:
                elements = []
                for element in getattr(self, item):
                    elements.append(f'{element.__repr__()}')
                str_list.append(f'{item}:\n' + "\n".join(elements))
                continue
            str_list.append(f'{item}: {getattr(self, item)}')
        return ', '.join(str_list)

    @classmethod
    def of_dict(cls, dict):
        for arg_name, arg_value in enumerate(dict):
           a = cls
        return Entity()