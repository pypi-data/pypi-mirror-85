from sys import stdout, argv

from casec.client import Client
from casec.command import RootCommandGroup, SnakeCaseCommand, CamelCaseCommand, PascalCaseCommand, KebabCaseCommand, \
    ConstantCaseCommand, DomainCommand, PathCommand, CsvCommand
from casec.container import CharacterType
from casec.operation import ParseCharacterDelimited, FormatCamelCase, FormatKebabCase, FormatPascalCase, \
    ParseCaseDelimited, \
    FormatSnakeCase, FormatConstantCase, FormatDomain, FormatPath, FormatCsv


def main(args=None):
    args = args or argv[1:]
    Client(
        RootCommandGroup(
            (
                SnakeCaseCommand(
                    (
                        ParseCharacterDelimited(CharacterType.UNDERSCORE),
                        FormatCamelCase(),
                        FormatPascalCase(),
                        FormatKebabCase(),
                        FormatConstantCase(),
                        FormatDomain(),
                        FormatPath(),
                        FormatCsv()
                    ),
                    stdout
                ),
                CamelCaseCommand(
                    (
                        ParseCaseDelimited(CharacterType.UPPERCASE),
                        FormatSnakeCase(),
                        FormatPascalCase(),
                        FormatKebabCase(),
                        FormatConstantCase(),
                        FormatDomain(),
                        FormatPath(),
                        FormatCsv()
                    ),
                    stdout
                ),
                PascalCaseCommand(
                    (
                        ParseCaseDelimited(CharacterType.UPPERCASE),
                        FormatSnakeCase(),
                        FormatCamelCase(),
                        FormatKebabCase(),
                        FormatConstantCase(),
                        FormatDomain(),
                        FormatPath(),
                        FormatCsv()
                    ),
                    stdout
                ),
                KebabCaseCommand(
                    (
                        ParseCharacterDelimited(CharacterType.DASH),
                        FormatSnakeCase(),
                        FormatCamelCase(),
                        FormatPascalCase(),
                        FormatConstantCase(),
                        FormatDomain(),
                        FormatPath(),
                        FormatCsv()
                    ),
                    stdout
                ),
                ConstantCaseCommand(
                    (
                        ParseCharacterDelimited(CharacterType.UNDERSCORE),
                        FormatSnakeCase(),
                        FormatCamelCase(),
                        FormatPascalCase(),
                        FormatKebabCase(),
                        FormatDomain(),
                        FormatPath(),
                        FormatCsv()
                    ),
                    stdout
                ),
                PathCommand(
                    (
                        ParseCharacterDelimited(CharacterType.SLASH),
                        FormatSnakeCase(),
                        FormatCamelCase(),
                        FormatPascalCase(),
                        FormatConstantCase(),
                        FormatKebabCase(),
                        FormatDomain(),
                        FormatCsv()
                    ),
                    stdout
                ),
                DomainCommand(
                    (
                        ParseCharacterDelimited(CharacterType.DOT),
                        FormatSnakeCase(),
                        FormatCamelCase(),
                        FormatPascalCase(),
                        FormatConstantCase(),
                        FormatPath(),
                        FormatKebabCase(),
                        FormatCsv()
                    ),
                    stdout
                ),
                CsvCommand(
                    (
                        ParseCharacterDelimited(CharacterType.COMMA),
                        FormatSnakeCase(),
                        FormatCamelCase(),
                        FormatPascalCase(),
                        FormatConstantCase(),
                        FormatPath(),
                        FormatKebabCase(),
                        FormatDomain()
                    ),
                    stdout
                )
            )
        )
    ).run(args)


if __name__ == '__main__':
    main(argv[1:])
