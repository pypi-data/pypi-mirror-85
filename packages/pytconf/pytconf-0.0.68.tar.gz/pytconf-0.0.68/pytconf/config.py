import itertools
import json
import os
import sys
from collections import defaultdict
from typing import Union, List, Any, Callable, Type, Dict, Set

from yattag import Doc

from pytconf.color_utils import (
    print_highlight,
    color_hi,
    print_title,
    color_ok,
    color_warn,
    print_error,
)
from pytconf.errors_collector import ErrorsCollector
from pytconf.param import Param, NO_DEFAULT
from pytconf.pydoc import get_first_line
from pytconf.utils import get_logger

PARAMS_ATTRIBUTE = "_params"

DEFAULT_FUNCTION_GROUP_NAME = "default"
DEFAULT_FUNCTION_GROUP_DESCRIPTION = "default command group"
DEFAULT_FUNCTION_GROUP_SHOW_META = False
DEFAULT_FUNCTION_GROUP_SHOW = True

SPECIAL_FUNCTION_GROUP_NAME = "special"
SPECIAL_FUNCTION_GROUP_DESCRIPTION = "special command group"
SPECIAL_FUNCTION_GROUP_SHOW_META = False
SPECIAL_FUNCTION_GROUP_SHOW = False

DEFAULT_FUNCTION_DESCRIPTION = "No function description available"


class MetaConfig(type):
    """
    Meta class for all configs
    """

    def __new__(mcs, name, bases, cls_dict):
        if name != "Config":
            params_dict = dict()
            cls_dict[PARAMS_ATTRIBUTE] = params_dict
            for k, d in cls_dict.items():
                if isinstance(d, Param):
                    # assert d.default is not NO_DEFAULT
                    params_dict[k] = d
                    cls_dict[k] = d.default
        return type.__new__(mcs, name, bases, cls_dict)

    def __init__(cls, name, bases, cls_dict):
        # print(name, bases, cls_dict)
        # if len(cls.mro()) > 2:
        #     register_config(cls, name)
        #     # print("was subclassed by " + name)
        if name != "Config":
            # noinspection PyTypeChecker
            get_pytconf().register_config(cls, name)
        # print(name, cls_dict)
        super(MetaConfig, cls).__init__(name, bases, cls_dict)


class Config(metaclass=MetaConfig):
    """
    Base class for all configs
    """

    @classmethod
    def get_attributes(cls: Any) -> List[str]:
        return getattr(cls, PARAMS_ATTRIBUTE).keys()

    @classmethod
    def get_params(cls: Any) -> Dict[str, Param]:
        return getattr(cls, PARAMS_ATTRIBUTE)

    @classmethod
    def get_param_by_name(cls: Any, name: str) -> Param:
        return cls.get_params()[name]


class HtmlGen:
    def __init__(self):
        document, tag, text, line = Doc().ttl()
        self.document = document
        self.tag = tag
        self.text = text
        self.line = line


def is_help(string: str) -> bool:
    return string.lower()[:4] == "help"


class PytconfConf:
    def __init__(self):
        self._configs = set()
        self._config_names = set()
        self.main_function: Union[Callable, None] = None
        self.main_description: str = "No application description"
        self.function_name_to_configs: Dict[str, List[Type[Config]]] = dict()
        self.function_name_to_suggest_configs: Dict[str, List[Type[Config]]] = dict()
        self.function_name_to_callable: Dict[str, Callable] = dict()
        self.allow_free_args: Dict[str, bool] = dict()
        self.min_free_args: Dict[str, Union[int, None]] = dict()
        self.max_free_args: Dict[str, Union[int, None]] = dict()
        self.description: Dict[str, str] = dict()

        self.function_group_names: Dict[str, Set[str]] = defaultdict(set)
        self.function_group_list: List[str] = []
        self.function_group_descriptions: Dict[str, str] = dict()
        self.function_group_show_meta: Dict[str, bool] = dict()
        self.function_group_show: Dict[str, bool] = dict()

        self.attribute_to_config: Dict[str, Type[Config]] = dict()
        self.free_args: List[str] = []
        self.app_name: str = "No application name"
        self.version: str = "No version"

    def register_main(
        self,
        main_function: Callable,
        main_description: str,
        app_name: str,
        version: str,
    ):
        self.main_function = main_function
        self.main_description = main_description
        self.app_name = app_name
        self.version = version

    def register_function(
        self,
        function: Callable,
        description: str,
        name: str,
        configs: List[Type[Config]] = (),
        suggest_configs: List[Type[Config]] = (),
        group: Union[str, None] = None,
        allow_free_args: bool = False,
        min_free_args: Union[int, None] = None,
        max_free_args: Union[int, None] = None,
    ):
        self.description[name] = description
        self.function_name_to_callable[name] = function
        self.function_name_to_configs[name] = configs
        self.function_name_to_suggest_configs[name] = suggest_configs
        self.function_group_names[group].add(name)
        self.allow_free_args[name] = allow_free_args
        self.min_free_args[name] = min_free_args
        self.max_free_args[name] = max_free_args

    def register_config(self, config: Type[Config], name):
        """
        register a configuration class
        :param config:
        :param name:
        :return:
        """
        self._configs.add(config)
        self._config_names.add(name)
        # update the attributes_to_config map
        for attribute in config.get_attributes():
            if attribute in self.attribute_to_config:
                raise ValueError(
                    f"pytconf: attribute [{attribute}] appears more than once"
                )
            self.attribute_to_config[attribute] = config

    @classmethod
    def print_errors(cls, errors: ErrorsCollector) -> None:
        for error in errors.yield_errors():
            print_error(error)

    def show_help(self) -> None:
        print(f"Usage: {color_hi(self.app_name)} COMMAND [ARGS]...")
        space = " " * 2
        print_highlight(f"\n{space}{self.main_description}\n")
        for function_group in self.function_group_list:
            show = self.function_group_show[function_group]
            if not show:
                continue
            show_meta = self.function_group_show_meta[function_group]
            if show_meta:
                description = self.function_group_descriptions[function_group]
                print(f"{space}{function_group}: {description}")
                cmd_space = space + " " * 2
            else:
                cmd_space = space
            for name in sorted(self.function_group_names[function_group]):
                function_doc = self.description[name]
                print(f"{cmd_space}{color_hi(name)}: {function_doc}")
            print()

    def show_help_for_function(
        self,
        function_name: str,
        show_help_full: bool = False,
        show_help_suggest: bool = False,
    ) -> None:
        print(f"Usage: {self.app_name} {function_name} [OPTIONS] [ARGS]...")
        function_doc = self.description[function_name]
        print_highlight(f"\n  {function_doc}")
        print("\nOptions:\n")
        for config in self.function_name_to_configs[function_name]:
            self.show_help_for_config(config)
        if show_help_suggest:
            for config in self.function_name_to_suggest_configs[function_name]:
                self.show_help_for_config(config)
        if show_help_full:
            for config in self._configs:
                self.show_help_for_config(config)

    @classmethod
    def show_help_for_config(cls, config):
        if config == Config:
            return
        doc = get_first_line(config.__doc__)
        if doc is not None:
            print_title(f"  {doc}")
        else:
            print_title("  Undocumented parameter set")
        for name, param in config.get_params().items():
            if param.default is NO_DEFAULT:
                default = color_warn("MANDATORY")
            else:
                default = color_ok(param.t2s(param.default))
            print(f"    {color_hi(name)} [{param.get_type_name()}]: {param.help_string} [{default}]")
            more_help = param.more_help()
            if more_help is not None:
                print(f"      {more_help}")
        print()

    def process_flags(
        self, function_selected: str, flags: Dict[str, str], errors: ErrorsCollector,
    ) -> None:
        """
        Parse the args and fill the global data
        :param function_selected:
        :param flags:
        :param errors:
        """

        # set the flags into the "default" field and collect unknown flags
        unknown_flags = []
        for flag_raw, value in flags.items():
            if flag_raw not in self.attribute_to_config:
                if is_help(flag_raw):
                    errors.set_do_help()
                    errors.unset_show_errors()
                else:
                    unknown_flags.append(flag_raw)
                continue
            config = self.attribute_to_config[flag_raw]
            param = config.get_param_by_name(flag_raw)
            edit = value.startswith("=")
            if edit:
                v = param.s2t_generate_from_default(value[1:])
            else:
                v = param.s2t(value)
            setattr(config, flag_raw, v)
        if unknown_flags:
            errors.add_error(f"unknown flags [{','.join(unknown_flags)}]")

        # check for missing parameters
        missing_parameters = []
        configs = self.function_name_to_configs[function_selected]
        for config in configs:
            for attribute in config.get_attributes():
                value = getattr(config, attribute)
                if value is NO_DEFAULT:
                    missing_parameters.append(attribute)
        if missing_parameters:
            errors.add_error(
                f"missing parameters [{','.join(missing_parameters)}]"
            )

        # move all default values to place (this will not be needed in the new scheme)
        for config in itertools.chain(configs, self._configs):
            for attribute in config.get_attributes():
                param: Param = getattr(config, attribute)
                if isinstance(param, Param):
                    if param.default is not NO_DEFAULT:
                        setattr(config, attribute, param.default)

    @staticmethod
    def read_flags_from_config(file_name: str, flags: Dict[str, str]) -> None:
        if os.path.isfile(file_name):
            with open(file_name, "rt") as json_file:
                new_flags: Dict[str, str] = json.load(json_file)
                assert isinstance(flags, dict)
            for k, v in new_flags.items():
                flags[k] = v

    def get_system_config(self):
        return f"/etc/{self.app_name}.json"

    def get_user_config(self):
        return os.path.expanduser(f"~/.config/{self.app_name}.json")

    def register_function_group(
        self,
        name: str,
        description: str,
        show_meta: bool,
        show: bool,
    ):
        self.function_group_list.append(name)
        self.function_group_descriptions[name] = description
        self.function_group_show_meta[name] = show_meta
        self.function_group_show[name] = show

    def register_defaults(self):
        self.register_function_group(
            name=DEFAULT_FUNCTION_GROUP_NAME,
            description=DEFAULT_FUNCTION_GROUP_DESCRIPTION,
            show_meta=DEFAULT_FUNCTION_GROUP_SHOW_META,
            show=DEFAULT_FUNCTION_GROUP_SHOW,
        )
        self.register_function_group(
            name=SPECIAL_FUNCTION_GROUP_NAME,
            description=SPECIAL_FUNCTION_GROUP_DESCRIPTION,
            show_meta=SPECIAL_FUNCTION_GROUP_SHOW_META,
            show=SPECIAL_FUNCTION_GROUP_SHOW,
        )

    def get_function_selected(self, args: List[str], errors) -> Union[str, None]:
        function_selected = None
        if len(args) > 0:
            command = args.pop(0)
            if command in self.function_name_to_callable:
                function_selected = command
            else:
                if is_help(command):
                    errors.set_do_help()
                    errors.unset_show_errors()
                else:
                    errors.add_error(f"unknown command [{command}]")
                    errors.set_force_show_errors()
        return function_selected

    def config_arg_parse_and_launch(
        self,
        args: Union[List[str], None] = None,
        launch=True,
        do_exit=True,
    ) -> None:

        self.register_defaults()
        if args is None:
            args = sys.argv[1:]

        flags: Dict[str, str] = dict()
        errors = ErrorsCollector()
        self.free_args = []

        # read config files
        self.read_flags_from_config(file_name=self.get_system_config(), flags=flags)
        self.read_flags_from_config(file_name=self.get_user_config(), flags=flags)

        function_selected = self.get_function_selected(args, errors)

        # now parse the args
        self.parse_args(args, errors, flags)

        # if we have command we can check free args errors
        if function_selected is not None:
            if self.allow_free_args[function_selected]:
                min_args = self.min_free_args[function_selected]
                if min_args is not None:
                    if len(self.free_args) < min_args:
                        errors.add_error(f"too few free args - {min_args} required")
                max_args = self.max_free_args[function_selected]
                if max_args is not None:
                    if len(self.free_args) >= max_args:
                        errors.add_error(f"too many free args - {max_args} required")
            else:
                if len(self.free_args) > 0:
                    if len(self.free_args) == 1 and is_help(self.free_args[0]):
                        errors.set_do_help()
                        errors.unset_show_errors()
                    else:
                        errors.add_error(f"free args are not allowed [{self.free_args}]")

        if function_selected is None:
            errors.add_error("no command is selected")
            errors.set_do_help()
            errors.unset_show_errors()
        else:
            self.process_flags(function_selected, flags, errors)

        if errors.have_errors() or errors.get_do_help():
            if errors.get_show_errors():
                self.print_errors(errors)
            if errors.get_do_help():
                if function_selected:
                    self.show_help_for_function(function_name=function_selected)
                else:
                    self.show_help()
            if do_exit:
                sys.exit(1)
            return

        if launch:
            function_to_run = self.function_name_to_callable[function_selected]
            function_to_run()

    def parse_args(self, args, errors, flags):
        free_args_started = False
        while args:
            current = args.pop(0)
            if current.startswith("--") and not free_args_started:
                real = current[2:]
                number_of_equals = real.count("=")
                if number_of_equals == 1:
                    flag_name, flag_value = real.split("=")
                    flags[flag_name] = flag_value
                elif number_of_equals == 0:
                    if args:
                        more = args.pop(0)
                        flags[real] = more
                    else:
                        errors.add_error(
                            f"argument [{real}] needs a follow-up argument"
                        )
                else:
                    errors.add_error(f"can not parse argument [{real}]")
            else:
                self.free_args.append(current)
                free_args_started = True

    def get_html(self) -> str:
        html_gen = HtmlGen()
        main_doc = self.main_description
        html_gen.line("h1", main_doc)
        html_gen.line("h2", "API specifications")
        single_group = len(self.function_group_list) == 1
        with html_gen.tag("ul"):
            for function_group_name in self.function_group_list:
                if not single_group:
                    function_group_description = self.function_group_descriptions[
                        function_group_name
                    ]
                    html_gen.line("li", function_group_name, title="function group name: ")
                    html_gen.line(
                        "li",
                        function_group_description,
                        title="function group description: ",
                    )
                with html_gen.tag("li"):
                    for function_name in sorted(
                        self.function_group_names[function_group_name]
                    ):
                        self.get_html_for_function(function_name, html_gen)
        return html_gen.document.getvalue()

    def get_html_for_function(self, function_name, html_gen):
        with html_gen.tag("ul"):
            f = self.function_name_to_callable[function_name]
            function_doc = get_first_line(f.__doc__)
            if function_doc is None:
                function_doc = "not description for this function"
            html_gen.line("li", function_name, title="function name: ")
            html_gen.line("li", function_doc, title="function description: ")
            with html_gen.tag("li"):
                with html_gen.tag("ul"):
                    for config in self.function_name_to_configs[function_name]:
                        with html_gen.tag("li"):
                            self.get_html_for_config(config, html_gen)

    @classmethod
    def get_html_for_config(cls, config, html_gen):
        if config == Config:
            return
        doc = get_first_line(config.__doc__)
        if doc is None:
            doc = "undocumented config"
        html_gen.line("h3", doc, title="config: ")
        with html_gen.tag("table"):
            for name, param in config.get_params().items():
                with html_gen.tag("tr"):
                    if param.default is NO_DEFAULT:
                        default = "MANDATORY"
                    else:
                        default = param.t2s(param.default)
                    if param.more_help() is None:
                        more_help = "No more help is documented"
                    else:
                        more_help = param.more_help()
                    html_gen.line("td", name)
                    html_gen.line("td", param.help_string)
                    html_gen.line("td", param.get_type_name())
                    html_gen.line("td", default)
                    html_gen.line("td", more_help)

    def write_config_file_json(self, filename: str) -> None:
        values: Dict[str, str] = dict()
        for config in self._configs:
            for name, param in config.get_params().items():
                if param.default is not NO_DEFAULT:
                    values[name] = param.t2s(param.default)
        with open(filename, "wt") as f:
            json.dump(values, f, indent=4)

    def write_config_file_json_user(self) -> None:
        self.write_config_file_json(self.get_user_config())

    def write_config_file_json_system(self) -> None:
        self.write_config_file_json(self.get_system_config())


_pytconf = PytconfConf()


def get_pytconf():
    return _pytconf


def config_arg_parse_and_launch(
    args=None,
    launch=True,
    do_exit=True,
) -> None:
    """
    This is the real API
    """
    get_pytconf().config_arg_parse_and_launch(
        args=args,
        launch=launch,
        do_exit=do_exit,
    )


def get_free_args() -> List[str]:
    return get_pytconf().free_args


# TODO: remove default values for next function when ready to force
# TODO: change function_group_name -> name
# TODO: change function_group_description -> description
def register_function_group(
    function_group_name: str,
    function_group_description: str,
    show_meta: bool = True,
    show: bool = True,
) -> None:
    get_pytconf().register_function_group(
        name=function_group_name,
        description=function_group_description,
        show_meta=show_meta,
        show=show,
    )


def register_main(
    main_description: str = "NO DESCRIPTION",  # TODO: remove when ready to force
    app_name: str = "NO APP",  # TODO: remove when ready to force
    version: str = "NO VERSION",  # TODO: remove when ready to force
) -> Callable[[Any], Any]:
    def identity(main_function):
        get_pytconf().register_main(
            main_function=main_function,
            main_description=main_description,
            app_name=app_name,
            version=version,
        )
        return main_function

    return identity


def register_endpoint(
    description: str = "No description",  # TODO: remove default value
    name: Union[str, None] = None,
    configs: List[Type[Config]] = (),
    suggest_configs: List[Type[Config]] = (),
    group: str = DEFAULT_FUNCTION_GROUP_NAME,
    allow_free_args: bool = False,
    min_free_args: Union[int, None] = None,
    max_free_args: Union[int, None] = None,
) -> Callable[[Any], Any]:
    logger = get_logger()
    logger.debug("registering endpoint")

    def identity(function):
        if name is None:
            function_name = function.__name__
        else:
            function_name = name
        register_function(
            function=function,
            description=description,
            name=function_name,
            configs=configs,
            suggest_configs=suggest_configs,
            group=group,
            allow_free_args=allow_free_args,
            min_free_args=min_free_args,
            max_free_args=max_free_args,
        )
        return function

    return identity


def register_function(
    function: Callable,
    description: str,
    name: str,
    configs: List[Type[Config]] = (),
    suggest_configs: List[Type[Config]] = (),
    group: Union[str, None] = None,
    allow_free_args: bool = False,
    min_free_args: Union[int, None] = None,
    max_free_args: Union[int, None] = None,
) -> None:
    get_pytconf().register_function(
        function=function,
        description=description,
        name=name,
        configs=configs,
        suggest_configs=suggest_configs,
        group=group,
        allow_free_args=allow_free_args,
        min_free_args=min_free_args,
        max_free_args=max_free_args,
    )


def write_config_file_json_user() -> None:
    filename = get_pytconf().get_user_config()
    if not os.path.isfile(filename):
        get_pytconf().write_config_file_json_user()


def rm_config_file_json_user() -> None:
    filename = get_pytconf().get_user_config()
    if os.path.isfile(filename):
        os.unlink(filename)


def write_config_file_json_system() -> None:
    filename = get_pytconf().get_system_config()
    if not os.path.isfile(filename):
        get_pytconf().write_config_file_json_system()


def rm_config_file_json_system() -> None:
    filename = get_pytconf().get_system_config()
    if os.path.isfile(filename):
        os.unlink(filename)
