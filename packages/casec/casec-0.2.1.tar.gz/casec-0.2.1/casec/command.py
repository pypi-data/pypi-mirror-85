from abc import ABC, abstractmethod
from argparse import Namespace, ArgumentParser, FileType, Action
from sys import stdout, stdin
from typing import Optional, Dict, Tuple, List

from casec.operation import OperationInterface


class CommaSeparatedListAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))


class CommandMetaInterface(ABC):
    @property
    @abstractmethod
    def help(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def usage(self) -> Optional[str]:
        raise NotImplementedError


class CommandInterface(CommandMetaInterface, ABC):
    @property
    @abstractmethod
    def defaults(self) -> Dict:
        raise NotImplementedError

    @property
    @abstractmethod
    def options(self) -> Tuple[Dict, ...]:
        raise NotImplementedError

    @abstractmethod
    def execute(self, namespace: Namespace):
        raise NotImplementedError


class CommandGroupInterface(CommandMetaInterface, ABC):
    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def metavar(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def subcommands(self) -> Tuple[CommandMetaInterface, ...]:
        raise NotImplementedError

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_parents(self, base_parser: ArgumentParser) -> List[ArgumentParser]:
        raise NotImplementedError


class CommandBase(CommandInterface, ABC):
    def __init__(
            self,
            operations: Tuple[OperationInterface, ...],
            out: stdout
    ):
        self.operations = operations
        self.out = out

    @property
    def defaults(self) -> Dict:
        return {}

    @property
    def usage(self) -> Optional[str]:
        return None

    def execute(self, namespace: Namespace):
        for operation in self.operations:
            operation.should_perform(namespace) and operation.perform(namespace)

        self.out.write('\n'.join(namespace.formatted_strings))


class CommandGroupBase(CommandGroupInterface, ABC):
    def __init__(self, subcommands: Tuple[CommandMetaInterface, ...]):
        self._subcommands = subcommands

    @property
    def subcommands(self) -> Tuple[CommandMetaInterface, ...]:
        return self._subcommands

    @property
    def usage(self) -> Optional[str]:
        return None

    def get_parents(self, base_parser: ArgumentParser) -> List[ArgumentParser]:
        return [base_parser]


class RootCommandGroup(CommandGroupBase):
    @property
    def description(self) -> str:
        return 'Convert the case of a string.'

    @property
    def metavar(self) -> str:
        return 'COMMAND'

    @property
    def help(self) -> str:
        return 'A case converter.'

    @property
    def name(self) -> str:
        return 'casec'

    @property
    def title(self) -> str:
        return 'Commands'

    @property
    def usage(self) -> Optional[str]:
        return 'casec COMMAND'


class SnakeCaseCommand(CommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('-f', '--file',),
                'kwargs': {
                    'default': stdin,
                    'dest': 'file_object',
                    'help': 'An input file which should be converted to another case. May also be stdin.',
                    'type': FileType('r')
                }
            },
            {
                'args': ('-c', '--camel-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_camel_case',
                    'help': 'Convert the input to camel case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-p', '--pascal-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_pascal_case',
                    'help': 'Convert the input to pascal case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-k', '--kebab-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_kebab_case',
                    'help': 'Convert the input to kebab case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-d', '--domain'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_domain',
                    'help': 'Convert the input to domain syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-t', '--path'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_path',
                    'help': 'Convert the input to path syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-v', '--csv'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_csv',
                    'help': 'Convert the input to a comma separated list.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-o', '--constant-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_constant_case',
                    'help': 'Convert the input to constant case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-r', '--format-literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'format_literals',
                    'help': 'A comma separated list of case sensitive string literals. During formatting, any words '
                            'which match a lower cased literal will formatted with the same casing as the literal.'

                }
            }
        )

    @property
    def help(self) -> str:
        return 'Convert the case of snake case strings.'

    @property
    def name(self) -> str:
        return 'snake-case'


class CamelCaseCommand(CommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('-f', '--file',),
                'kwargs': {
                    'default': stdin,
                    'dest': 'file_object',
                    'help': 'An input file which should be converted to another case. May also be stdin.',
                    'type': FileType('r')
                }
            },
            {
                'args': ('-s', '--snake-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_snake_case',
                    'help': 'Convert the input to snake case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-p', '--pascal-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_pascal_case',
                    'help': 'Convert the input to pascal case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-k', '--kebab-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_kebab_case',
                    'help': 'Convert the input to kebab case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-d', '--domain'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_domain',
                    'help': 'Convert the input to domain syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-t', '--path'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_path',
                    'help': 'Convert the input to path syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-v', '--csv'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_csv',
                    'help': 'Convert the input to a comma separated list.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-o', '--constant-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_constant_case',
                    'help': 'Convert the input to constant case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-r', '--format-literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'format_literals',
                    'help': 'A comma separated list of case sensitive string literals. During formatting, any words '
                            'which match a lower cased literal will formatted with the same casing as the literal.'
                }
            },
            {
                'args': ('-l', '--literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'literals',
                    'help': 'A comma separated list of case sensitive string literals that should be treated as a word '
                            'when parsing input.'
                }
            }
        )

    @property
    def help(self) -> str:
        return 'Convert the case of camel case strings.'

    @property
    def name(self) -> str:
        return 'camel-case'


class PascalCaseCommand(CommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('-f', '--file',),
                'kwargs': {
                    'default': stdin,
                    'dest': 'file_object',
                    'help': 'An input file which should be converted to another case. May also be stdin.',
                    'type': FileType('r')
                }
            },
            {
                'args': ('-c', '--camel-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_camel_case',
                    'help': 'Convert the input to camel case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-s', '--snake-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_snake_case',
                    'help': 'Convert the input to snake case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-k', '--kebab-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_kebab_case',
                    'help': 'Convert the input to kebab case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-d', '--domain'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_domain',
                    'help': 'Convert the input to domain syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-t', '--path'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_path',
                    'help': 'Convert the input to path syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-o', '--constant-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_constant_case',
                    'help': 'Convert the input to constant case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-v', '--csv'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_csv',
                    'help': 'Convert the input to a comma separated list.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-r', '--format-literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'format_literals',
                    'help': 'A comma separated list of case sensitive string literals. During formatting, any words '
                            'which match a lower cased literal will formatted with the same casing as the literal.'
                }
            },
            {
                'args': ('-l', '--literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'literals',
                    'help': 'A comma separated list of case sensitive string literals that should be treated as a word '
                            'when parsing input.'
                }
            }
        )

    @property
    def help(self) -> str:
        return 'Convert the case of pascal case strings.'

    @property
    def name(self) -> str:
        return 'pascal-case'


class ConstantCaseCommand(CommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('-f', '--file',),
                'kwargs': {
                    'default': stdin,
                    'dest': 'file_object',
                    'metavar': '<file>',
                    'help': 'An input file which should be converted to another case. May also be stdin.',
                    'type': FileType('r')
                }
            },
            {
                'args': ('-c', '--camel-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_camel_case',
                    'help': 'Convert the input to camel case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-p', '--pascal-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_pascal_case',
                    'help': 'Convert the input to pascal case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-s', '--snake-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_snake_case',
                    'help': 'Convert the input to snake case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-k', '--kebab-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_kebab_case',
                    'help': 'Convert the input to kebab case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-d', '--domain'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_domain',
                    'help': 'Convert the input to domain syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-t', '--path'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_path',
                    'help': 'Convert the input to path syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-v', '--csv'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_csv',
                    'help': 'Convert the input to a comma separated list.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-r', '--format-literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'format_literals',
                    'help': 'A comma separated list of case sensitive string literals. During formatting, any words '
                            'which match a lower cased literal will formatted with the same casing as the literal.'
                }
            }
        )

    @property
    def help(self) -> str:
        return 'Convert the case of kebab case strings.'

    @property
    def name(self) -> str:
        return 'constant-case'


class KebabCaseCommand(CommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('-f', '--file',),
                'kwargs': {
                    'default': stdin,
                    'dest': 'file_object',
                    'metavar': '<file>',
                    'help': 'An input file which should be converted to another case. May also be stdin.',
                    'type': FileType('r')
                }
            },
            {
                'args': ('-c', '--camel-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_camel_case',
                    'help': 'Convert the input to camel case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-p', '--pascal-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_pascal_case',
                    'help': 'Convert the input to pascal case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-s', '--snake-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_snake_case',
                    'help': 'Convert the input to snake case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-d', '--domain'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_domain',
                    'help': 'Convert the input to domain syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-t', '--path'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_path',
                    'help': 'Convert the input to path syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-v', '--csv'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_csv',
                    'help': 'Convert the input to a comma separated list.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-o', '--constant-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_constant_case',
                    'help': 'Convert the input to constant case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-r', '--format-literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'format_literals',
                    'help': 'A comma separated list of case sensitive string literals. During formatting, any words '
                            'which match a lower cased literal will formatted with the same casing as the literal.'
                }
            }
        )

    @property
    def help(self) -> str:
        return 'Convert the case of kebab case strings.'

    @property
    def name(self) -> str:
        return 'kebab-case'


class DomainCommand(CommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('-f', '--file',),
                'kwargs': {
                    'default': stdin,
                    'dest': 'file_object',
                    'metavar': '<file>',
                    'help': 'An input file which should be converted to another case. May also be stdin.',
                    'type': FileType('r')
                }
            },
            {
                'args': ('-c', '--camel-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_camel_case',
                    'help': 'Convert the input to camel case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-p', '--pascal-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_pascal_case',
                    'help': 'Convert the input to pascal case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-s', '--snake-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_snake_case',
                    'help': 'Convert the input to snake case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-k', '--kebab-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_kebab_case',
                    'help': 'Convert the input to kebab case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-t', '--path'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_path',
                    'help': 'Convert the input to path syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-o', '--constant-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_constant_case',
                    'help': 'Convert the input to constant case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-v', '--csv'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_csv',
                    'help': 'Convert the input to a comma separated list.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-r', '--format-literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'format_literals',
                    'help': 'A comma separated list of case sensitive string literals. During formatting, any words '
                            'which match a lower cased literal will formatted with the same casing as the literal.'
                }
            }
        )

    @property
    def help(self) -> str:
        return 'Convert the case of domain strings.'

    @property
    def name(self) -> str:
        return 'domain'


class PathCommand(CommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('-f', '--file',),
                'kwargs': {
                    'default': stdin,
                    'dest': 'file_object',
                    'metavar': '<file>',
                    'help': 'An input file which should be converted to another case. May also be stdin.',
                    'type': FileType('r')
                }
            },
            {
                'args': ('-c', '--camel-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_camel_case',
                    'help': 'Convert the input to camel case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-p', '--pascal-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_pascal_case',
                    'help': 'Convert the input to pascal case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-s', '--snake-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_snake_case',
                    'help': 'Convert the input to snake case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-k', '--kebab-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_kebab_case',
                    'help': 'Convert the input to kebab case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-d', '--domain'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_domain',
                    'help': 'Convert the input to domain syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-o', '--constant-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_constant_case',
                    'help': 'Convert the input to constant case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-v', '--csv'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_csv',
                    'help': 'Convert the input to a comma separated list.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-r', '--format-literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'format_literals',
                    'help': 'A comma separated list of case sensitive string literals. During formatting, any words '
                            'which match a lower cased literal will formatted with the same casing as the literal.'
                }
            }
        )

    @property
    def help(self) -> str:
        return 'Convert the case of path strings.'

    @property
    def name(self) -> str:
        return 'path'


class CsvCommand(CommandBase):
    @property
    def options(self) -> Tuple[Dict, ...]:
        return (
            {
                'args': ('-f', '--file',),
                'kwargs': {
                    'default': stdin,
                    'dest': 'file_object',
                    'metavar': '<file>',
                    'help': 'An input file which should be converted to another case. May also be stdin.',
                    'type': FileType('r')
                }
            },
            {
                'args': ('-c', '--camel-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_camel_case',
                    'help': 'Convert the input to camel case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-p', '--pascal-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_pascal_case',
                    'help': 'Convert the input to pascal case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-s', '--snake-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_snake_case',
                    'help': 'Convert the input to snake case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-k', '--kebab-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_kebab_case',
                    'help': 'Convert the input to kebab case.'
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-d', '--domain'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_domain',
                    'help': 'Convert the input to domain syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-o', '--constant-case'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_constant_case',
                    'help': 'Convert the input to constant case.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-t', '--path'),
                'kwargs': {
                    'action': 'store_true',
                    'dest': 'format_path',
                    'help': 'Convert the input to path syntax.',
                },
                'mutually_exclusive_group': {
                    'name': 'format',
                    'is_required': True
                }
            },
            {
                'args': ('-r', '--format-literals'),
                'kwargs': {
                    'action': CommaSeparatedListAction,
                    'default': [],
                    'dest': 'format_literals',
                    'help': 'A comma separated list of case sensitive string literals. During formatting, any words '
                            'which match a lower cased literal will formatted with the same casing as the literal.'
                }
            }
        )

    @property
    def help(self) -> str:
        return 'Transform comma separated strings into another format.'

    @property
    def name(self) -> str:
        return 'csv'
