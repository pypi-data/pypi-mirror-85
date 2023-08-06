import abc
from enum import Enum
from typing import List, Union, Callable, Any, Type

from pytconf.enum_subset import EnumSubset

from pytconf.extended_enum import str_to_enum_value, enum_type_to_list_str

from pytconf.convert import convert_str_to_str, convert_str_to_int, convert_int_to_str, convert_str_to_int_default, \
    convert_str_to_list_int, convert_list_int_to_str, convert_str_to_list_str, convert_list_str_to_str, \
    convert_str_to_int_or_none, convert_int_or_none_to_str, convert_str_to_str_or_none, convert_str_or_none_to_str, \
    convert_str_to_bool, convert_bool_to_str


class Unique:
    pass


NO_DEFAULT = Unique()
NO_DEFAULT_TYPE = type(NO_DEFAULT)
NO_HELP = "No help for this configuration option"


class Param:
    __metaclass__ = abc.ABCMeta
    """
        Parent class of all parameters of configuration
    """

    def __init__(
        self, help_string=NO_HELP, default=NO_DEFAULT, type_name=None,
    ):
        super().__init__()
        self.help_string = help_string
        self.default = default
        self.type_name = type_name

    def get_type_name(self):
        return self.type_name

    @abc.abstractmethod
    def s2t(self, s: str) -> object:
        pass

    def s2t_generate_from_default(self, s: str) -> object:
        raise ValueError("we do not support generation from default")

    @abc.abstractmethod
    def t2s(self, t: object) -> str:
        pass

    # noinspection PyMethodMayBeStatic
    def more_help(self) -> Union[str, None]:
        return None


class ParamFunctions(Param):
    """
    Parent class of all parameters of configuration
    """

    def __init__(
        self,
        help_string=NO_HELP,
        default=NO_DEFAULT,
        type_name=None,
        function_s2t: Callable = None,
        function_s2t_generate_from_default: Callable = None,
        function_t2s: Callable = None,
    ):
        super().__init__(
            help_string=help_string, default=default, type_name=type_name,
        )
        self.function_s2t = function_s2t
        self.function_t2s = function_t2s
        self.function_s2t_generate_from_default = function_s2t_generate_from_default

    def s2t(self, s: str) -> Any:
        return self.function_s2t(s)

    def s2t_generate_from_default(self, s: str) -> Any:
        return self.function_s2t_generate_from_default(self.default, s)

    def t2s(self, t: Any) -> str:
        return self.function_t2s(t)


class ParamFilename(Param):
    def __init__(
        self,
        help_string=NO_HELP,
        default=NO_DEFAULT,
        type_name=None,
        suffixes: List[str] = None,
    ):
        super().__init__(
            help_string=help_string, default=default, type_name=type_name,
        )
        self.suffixes = suffixes

    def s2t(self, s):
        if self.suffixes is not None:
            assert any(
                s.endswith(x) for x in self.suffixes
            ), "filename suffix is not accepted"
        return s

    def t2s(self, t):
        return t

    def more_help(self):
        if self.suffixes is None:
            return "no limitation on suffixes"
        return "allowed suffixes are {}".format(self.suffixes)


class ParamEnum(Param):
    def __init__(
        self, help_string=NO_HELP, default=NO_DEFAULT, enum_type: Type[Enum] = None,
    ):
        super().__init__(
            help_string=help_string, default=default, type_name="enum",
        )
        self.enum_type = enum_type

    def get_type_name(self):
        return "Enum[{}]".format(self.enum_type.__name__)

    def s2t(self, s: str) -> Any:
        return str_to_enum_value(s, self.enum_type)

    def t2s(self, t: Any) -> str:
        return t.name

    def more_help(self):
        return "allowed values {}".format(enum_type_to_list_str(self.enum_type))


class ParamEnumSubset(Param):
    def __init__(
        self, help_string=NO_HELP, default=NO_DEFAULT, enum_type: Type[Enum] = None,
    ):
        super().__init__(
            help_string=help_string, default=default, type_name="enum",
        )
        self.enum_type = enum_type

    def get_type_name(self):
        return "EnumSubset[{}]".format(self.enum_type.__name__)

    def s2t(self, s: str) -> EnumSubset:
        return EnumSubset.from_string(e=self.enum_type, s=s)

    def t2s(self, t: EnumSubset) -> str:
        return t.to_string()

    def s2t_generate_from_default(self, s: str) -> EnumSubset:
        pass

    def more_help(self):
        return "allowed values {}".format(enum_type_to_list_str(self.enum_type))


class ParamChoice(Param):
    def __init__(
        self, help_string=NO_HELP, default=NO_DEFAULT, choice_list: List[str] = None
    ):
        super().__init__(
            help_string=help_string, default=default, type_name="Choice",
        )
        self.choice_list = choice_list

    def s2t(self, s: str) -> Any:
        return s

    def t2s(self, t: Any) -> str:
        return t

    def more_help(self):
        return "allowed values {}".format(",".join(self.choice_list))


class ParamCreator:
    """
    Static namespace with all the param creation functions.
    """

    @staticmethod
    def create_int(
        help_string: str = NO_HELP, default: Union[int, NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> int:
        """
        Create an int parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="int",
            function_s2t=convert_str_to_int,
            function_t2s=convert_int_to_str,
            function_s2t_generate_from_default=convert_str_to_int_default,
        )

    @staticmethod
    def create_list_int(
        help_string: str = NO_HELP,
        default: Union[List[int], NO_DEFAULT_TYPE] = NO_DEFAULT,
    ) -> List[int]:
        """
        Create a List[int] parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="List[int]",
            function_s2t=convert_str_to_list_int,
            function_t2s=convert_list_int_to_str,
        )

    @staticmethod
    def create_list_str(
        help_string: str = NO_HELP,
        default: Union[List[str], NO_DEFAULT_TYPE] = NO_DEFAULT,
    ) -> List[str]:
        """
        Create a List[str] parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="List[str]",
            function_s2t=convert_str_to_list_str,
            function_t2s=convert_list_str_to_str,
        )

    @staticmethod
    def create_int_or_none(
        help_string: str = NO_HELP,
        default: Union[int, None, NO_DEFAULT_TYPE] = NO_DEFAULT,
    ) -> Union[int, None]:
        """
        Create an int parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="Union[int, None]",
            function_s2t=convert_str_to_int_or_none,
            function_t2s=convert_int_or_none_to_str,
        )

    @staticmethod
    def create_str(
        help_string: str = NO_HELP, default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> str:
        """
        Create a string parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="str",
            function_s2t=convert_str_to_str_or_none,
            function_t2s=convert_str_or_none_to_str,
        )

    @staticmethod
    def create_str_or_none(
        help_string: str = NO_HELP,
        default: Union[str, None, NO_DEFAULT_TYPE] = NO_DEFAULT,
    ) -> Union[str, None]:
        """
        Create a string parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="str",
            function_s2t=convert_str_to_str,
            function_t2s=convert_str_to_str,
        )

    @staticmethod
    def create_bool(
        help_string: str = NO_HELP, default: Union[bool, NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> bool:
        """
        Create a bool parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="bool",
            function_s2t=convert_str_to_bool,
            function_t2s=convert_bool_to_str,
        )

    @staticmethod
    def create_new_file(
        help_string: str = NO_HELP,
        default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT,
        suffixes: Union[List[str], None] = None,
    ) -> str:
        """
        Create a new file parameter
        :param help_string:
        :param default:
        :param suffixes:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFilename(
            help_string=help_string,
            default=default,
            type_name="new_file",
            suffixes=suffixes,
        )

    @staticmethod
    def create_existing_file(
        help_string: str = NO_HELP,
        default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT,
        suffixes: Union[List[str], None] = None,
    ) -> str:
        """
        Create a new file parameter
        :param help_string:
        :param default:
        :param suffixes:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFilename(
            help_string=help_string,
            default=default,
            type_name="existing_file",
            suffixes=suffixes,
        )

    @staticmethod
    def create_existing_folder(
        help_string: str = NO_HELP,
        default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT,
        suffixes: Union[List[str], None] = None,
    ) -> str:
        """
        Create a new folder parameter
        :param help_string:
        :param default:
        :param suffixes:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFilename(
            help_string=help_string,
            default=default,
            type_name="existing_folder",
            suffixes=suffixes,
        )

    @staticmethod
    def create_choice(
        choice_list: List[str],
        help_string: str = NO_HELP,
        default: Union[Any, NO_DEFAULT_TYPE] = NO_DEFAULT,
    ) -> str:
        """
        Create a choice config
        :param choice_list:
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamChoice(
            help_string=help_string, default=default, choice_list=choice_list,
        )

    @staticmethod
    def create_enum(
        enum_type: Type[Enum],
        help_string: str = NO_HELP,
        default: Union[Any, NO_DEFAULT_TYPE] = NO_DEFAULT,
    ) -> Type[Enum]:
        """
        Create an enum config
        :param enum_type:
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamEnum(help_string=help_string, default=default, enum_type=enum_type,)

    @staticmethod
    def create_enum_subset(
        enum_type: Type[Enum],
        help_string: str = NO_HELP,
        default: EnumSubset = NO_DEFAULT,
    ) -> EnumSubset:
        """
        Create an enum config
        :param enum_type:
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamEnumSubset(
            help_string=help_string, default=default, enum_type=enum_type,
        )

    @staticmethod
    def create_existing_bucket(
        help_string: str = NO_HELP, default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> str:
        """
        Create a bucket name on gcp
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="bucket_name",
            function_s2t=convert_str_to_str,
            function_t2s=convert_str_to_str,
        )
