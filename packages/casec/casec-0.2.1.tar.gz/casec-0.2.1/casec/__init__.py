from typing import List

from casec.container import CharacterType, CharacterContainer
from casec.formatter import CaseDelimitedFormatter, CharacterDelimitedFormatter
from casec.parser import CharacterDelimitedParser, CaseDelimitedParser


def parse_snake_case(string: str):
    return CharacterDelimitedParser(CharacterType.UNDERSCORE).parse(CharacterContainer(string))


def parse_camel_case(string: str, literals: List[str] = None):
    return CaseDelimitedParser(CharacterType.UPPERCASE, literals).parse(CharacterContainer(string))


def parse_pascal_case(string: str, literals: List[str] = None):
    return CaseDelimitedParser(CharacterType.UPPERCASE, literals).parse(CharacterContainer(string))


def parse_constant_case(string: str):
    return CharacterDelimitedParser(CharacterType.UNDERSCORE).parse(CharacterContainer(string))


def parse_kebab_case(string: str):
    return CharacterDelimitedParser(CharacterType.DASH).parse(CharacterContainer(string))


def parse_domain(string: str):
    return CharacterDelimitedParser(CharacterType.DOT).parse(CharacterContainer(string))


def parse_path(string: str):
    return CharacterDelimitedParser(CharacterType.SLASH).parse(CharacterContainer(string))


def snake_case_to_camel_case(string: str, format_literals: List[str]):
    words = parse_snake_case(string)
    return CaseDelimitedFormatter(CharacterType.LOWERCASE, format_literals).format(words)


def snake_case_to_pascal_case(string: str, format_literals: List[str]):
    words = parse_snake_case(string)
    return CaseDelimitedFormatter(CharacterType.UPPERCASE, format_literals).format(words)


def snake_case_to_constant_case(string: str):
    words = [CharacterContainer(str(word).upper()) for word in parse_snake_case(string)]
    return CharacterDelimitedFormatter('_').format(words)


def snake_case_to_kebab_case(string: str):
    words = parse_snake_case(string)
    return CharacterDelimitedFormatter('-').format(words)


def snake_case_to_domain(string: str):
    words = parse_snake_case(string)
    return CharacterDelimitedFormatter('.').format(words)


def snake_case_to_path(string: str):
    words = parse_snake_case(string)
    return CharacterDelimitedFormatter('/').format(words)


def camel_case_to_snake_case(string: str, literals: List[str] = None):
    words = parse_camel_case(string, literals)
    return CharacterDelimitedFormatter('_').format(words)


def camel_case_to_pascal_case(string: str, literals: List[str] = None, format_literals: List[str] = None):
    words = parse_camel_case(string, literals)
    return CaseDelimitedFormatter(CharacterType.UPPERCASE, format_literals).format(words)


def camel_case_to_constant_case(string: str, literals: List[str] = None):
    words = [CharacterContainer(str(word).upper()) for word in parse_camel_case(string, literals)]
    return CharacterDelimitedFormatter('_').format(words)


def camel_case_to_kebab_case(string: str, literals: List[str] = None):
    words = parse_camel_case(string, literals)
    return CharacterDelimitedFormatter('-').format(words)


def camel_case_to_domain(string: str, literals: List[str] = None):
    words = parse_camel_case(string, literals)
    return CharacterDelimitedFormatter('.').format(words)


def camel_case_to_path(string: str, literals: List[str] = None):
    words = parse_camel_case(string, literals)
    return CharacterDelimitedFormatter('/').format(words)


def pascal_case_to_snake_case(string: str, literals: List[str] = None):
    words = parse_pascal_case(string, literals)
    return CharacterDelimitedFormatter('_').format(words)


def pascal_case_to_camel_case(string: str, literals: List[str] = None, format_literals: List[str] = None):
    words = parse_pascal_case(string, literals)
    return CaseDelimitedFormatter(CharacterType.LOWERCASE, format_literals).format(words)


def pascal_case_to_constant_case(string: str, literals: List[str] = None):
    words = [CharacterContainer(str(word).upper()) for word in parse_pascal_case(string, literals)]
    return CharacterDelimitedFormatter('_').format(words)


def pascal_case_to_kebab_case(string: str, literals: List[str] = None):
    words = parse_pascal_case(string, literals)
    return CharacterDelimitedFormatter('-').format(words)


def pascal_case_to_domain(string: str, literals: List[str] = None):
    words = parse_pascal_case(string, literals)
    return CharacterDelimitedFormatter('.').format(words)


def pascal_case_to_path(string: str, literals: List[str] = None):
    words = parse_pascal_case(string, literals)
    return CharacterDelimitedFormatter('/').format(words)


def constant_case_to_snake_case(string: str):
    words = parse_constant_case(string)
    return CharacterDelimitedFormatter('_').format(words)


def constant_case_to_camel_case(string: str, format_literals: List[str]):
    words = parse_constant_case(string)
    return CaseDelimitedFormatter(CharacterType.LOWERCASE, format_literals).format(words)


def constant_case_to_pascal_case(string: str, format_literals: List[str]):
    words = parse_constant_case(string)
    return CaseDelimitedFormatter(CharacterType.UPPERCASE, format_literals).format(words)


def constant_case_to_kebab_case(string: str):
    words = parse_constant_case(string)
    return CharacterDelimitedFormatter('-').format(words)


def constant_case_to_domain(string: str):
    words = parse_constant_case(string)
    return CharacterDelimitedFormatter('.').format(words)


def constant_case_to_path(string: str):
    words = parse_constant_case(string)
    return CharacterDelimitedFormatter('/').format(words)


def kebab_case_to_snake_case(string: str):
    words = parse_kebab_case(string)
    return CharacterDelimitedFormatter('_').format(words)


def kebab_case_to_camel_case(string: str, format_literals: List[str]):
    words = parse_kebab_case(string)
    return CaseDelimitedFormatter(CharacterType.LOWERCASE, format_literals).format(words)


def kebab_case_to_pascal_case(string: str, format_literals: List[str]):
    words = parse_kebab_case(string)
    return CaseDelimitedFormatter(CharacterType.UPPERCASE, format_literals).format(words)


def kebab_case_to_constant_case(string: str):
    words = [CharacterContainer(str(word).upper()) for word in parse_kebab_case(string)]
    return CharacterDelimitedFormatter('_').format(words)


def kebab_case_to_domain(string: str):
    words = parse_kebab_case(string)
    return CharacterDelimitedFormatter('.').format(words)


def kebab_case_to_path(string: str):
    words = parse_kebab_case(string)
    return CharacterDelimitedFormatter('/').format(words)


def domain_to_snake_case(string: str):
    words = parse_domain(string)
    return CharacterDelimitedFormatter('_').format(words)


def domain_to_camel_case(string: str, format_literals: List[str]):
    words = parse_domain(string)
    return CaseDelimitedFormatter(CharacterType.LOWERCASE, format_literals).format(words)


def domain_to_pascal_case(string: str, format_literals: List[str]):
    words = parse_domain(string)
    return CaseDelimitedFormatter(CharacterType.UPPERCASE, format_literals).format(words)


def domain_to_constant_case(string: str):
    words = [CharacterContainer(str(word).upper()) for word in parse_domain(string)]
    return CharacterDelimitedFormatter('_').format(words)


def domain_to_kebab_case(string: str):
    words = parse_domain(string)
    return CharacterDelimitedFormatter('-').format(words)


def domain_to_path(string: str):
    words = parse_domain(string)
    return CharacterDelimitedFormatter('/').format(words)


def path_to_snake_case(string: str):
    words = parse_path(string)
    return CharacterDelimitedFormatter('_').format(words)


def path_to_camel_case(string: str, format_literals: List[str]):
    words = parse_path(string)
    return CaseDelimitedFormatter(CharacterType.LOWERCASE, format_literals).format(words)


def path_to_pascal_case(string: str, format_literals: List[str]):
    words = parse_path(string)
    return CaseDelimitedFormatter(CharacterType.UPPERCASE, format_literals).format(words)


def path_to_constant_case(string: str):
    words = [CharacterContainer(str(word).upper()) for word in parse_path(string)]
    return CharacterDelimitedFormatter('_').format(words)


def path_to_kebab_case(string: str):
    words = parse_path(string)
    return CharacterDelimitedFormatter('-').format(words)


def path_to_domain(string: str):
    words = parse_path(string)
    return CharacterDelimitedFormatter('.').format(words)
