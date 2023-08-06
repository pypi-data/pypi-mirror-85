from argparse import ArgumentParser, _SubParsersAction as SubParser, RawTextHelpFormatter
from typing import Tuple, Dict, List

from casec.command import CommandGroupInterface, CommandInterface, CommandMetaInterface


class ClientError(Exception):
    pass


class Client:
    options: Tuple[Dict] = tuple()

    def __init__(self, command_group: CommandGroupInterface):
        self.command_group = command_group
        self.parser: ArgumentParser = ArgumentParser(
            description=command_group.help,
            prog=command_group.name,
            usage=command_group.usage,
            formatter_class=RawTextHelpFormatter
        )
        self.base_parser = ArgumentParser(add_help=False)

    def run(self, *args):
        try:
            self._run(*args)
        except (KeyboardInterrupt, ClientError) as e:
            if isinstance(e, ClientError):
                print('Error: ', e)
            else:
                print('Exiting...')

    def _run(self, *args):
        self._set_global_options()
        command_group = self.command_group
        subparsers = self.parser.add_subparsers(
            title=command_group.title,
            description=command_group.description,
            metavar=command_group.metavar
        )
        self._set_commands(command_group.subcommands, subparsers, command_group.get_parents(self.base_parser))
        namespace = self.parser.parse_args(*args)

        if hasattr(namespace, 'command'):
            command: CommandInterface = namespace.command
            command.execute(namespace)
        elif hasattr(namespace, 'group_help'):
            namespace.group_help()
        else:
            self.parser.print_help()

    def _set_commands(
            self,
            commands: Tuple[CommandMetaInterface],
            subparsers: SubParser,
            parents: List[ArgumentParser]
    ):
        for command in commands:
            command_parser = subparsers.add_parser(
                command.name,
                help=command.help,
                parents=parents if isinstance(command, CommandInterface) else [],
                usage=command.usage
            )
            if isinstance(command, CommandInterface):
                self._set_command(command, command_parser)
            elif isinstance(command, CommandGroupInterface):
                command_parser.set_defaults(group_help=command_parser.print_help)
                self._set_command_group(command, command_parser)

    def _set_command(self, command: CommandInterface, command_parser: ArgumentParser):
        mutually_exclusive_groups = {}

        for option in command.options:
            if 'mutually_exclusive_group' in option:
                mutually_exclusive_group = option.get('mutually_exclusive_group')
                group_name = mutually_exclusive_group.get('name')
                is_required = mutually_exclusive_group.get('is_required') or False

                if group_name not in mutually_exclusive_groups:
                    mutually_exclusive_groups[group_name] = command_parser.add_mutually_exclusive_group(
                        required=is_required
                    )

                mutually_exclusive_groups[group_name].add_argument(*option.get('args'), **option.get('kwargs'))

            else:
                command_parser.add_argument(*option.get('args'), **option.get('kwargs'))

        command_parser.set_defaults(
            command=command,
            **command.defaults
        )

    def _set_command_group(
            self,
            command_group: CommandGroupInterface,
            command_parser: ArgumentParser
    ):
        subparsers = command_parser.add_subparsers(
            metavar=command_group.metavar,
            description=command_group.description,
            title=f"""
{command_group.help}

{command_group.title}\
"""
        )
        self._set_commands(command_group.subcommands, subparsers, command_group.get_parents(self.base_parser))

    def _set_global_options(self):
        argument_group = self.base_parser.add_argument_group('global arguments')
        for option in self.options:
            argument_group.add_argument(*option.get('args'), **option.get('kwargs'))
