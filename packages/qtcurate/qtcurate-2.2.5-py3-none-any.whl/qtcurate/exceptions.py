class QtConnectionError(Exception):
    pass


class QtRestApiError(Exception):
    """ Problem with authentification"""
    pass


class QtFileTypeError(Exception):
    """Invalid type of file"""
    pass



class QtArgumentError(Exception):
    pass


class QtVocabularyError(Exception):
    pass

class QtModelError(Exception):
    pass

class QtJobError(Exception):
    pass