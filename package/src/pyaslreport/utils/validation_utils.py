
class ValidationUtils:

    @staticmethod
    def is_valid_number(val):
        return isinstance(val, (int, float))

    @staticmethod
    def is_valid_list(val):
        return isinstance(val, list) and all(ValidationUtils.is_valid_number(v) for v in val)