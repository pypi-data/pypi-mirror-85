from abc import ABC, abstractmethod
from argparse import Namespace
from typing import IO

from casec.container import CharacterType, CharacterContainer
from casec.formatter import FormatterBase, CaseDelimitedFormatter, CharacterDelimitedFormatter
from casec.parser import CharacterDelimitedParser, CaseDelimitedParser, ParserBase


class OperationInterface(ABC):
    @abstractmethod
    def should_perform(self, namespace: Namespace):
        raise NotImplementedError

    @abstractmethod
    def perform(self, namespace: Namespace):
        raise NotImplementedError


class ParseBase(OperationInterface, ABC):
    def __init__(self, parser: ParserBase):
        self._parser = parser

    def perform(self, namespace: Namespace):
        parser = self._parser
        parsed_words = []
        file_object: IO = namespace.file_object

        with file_object as f:
            for line in f.readlines():
                parsed_words.append(parser.parse(CharacterContainer(line.strip())))

        namespace.parsed_words = parsed_words


class ParseCharacterDelimited(ParseBase):
    def __init__(self, delimiter: CharacterType):
        super().__init__(CharacterDelimitedParser(delimiter))

    def should_perform(self, namespace: Namespace):
        return True


class ParseCaseDelimited(ParseBase):
    def __init__(self, delimiter: CharacterType):
        super().__init__(CaseDelimitedParser(delimiter))

    def should_perform(self, namespace: Namespace):
        return True

    def perform(self, namespace: Namespace):
        if namespace.literals:
            self._parser.literals = namespace.literals

        super().perform(namespace)


class FormatBase(OperationInterface, ABC):
    def __init__(self, formatter: FormatterBase):
        self._formatter = formatter

    def perform(self, namespace: Namespace):
        formatter = self._formatter
        parsed_words = namespace.parsed_words
        formatted_strings = []

        for words in parsed_words:
            formatted_strings.append(formatter.format(words))

        namespace.formatted_strings = formatted_strings


class FormatSnakeCase(FormatBase):
    def __init__(self):
        super().__init__(CharacterDelimitedFormatter('_'))

    def should_perform(self, namespace: Namespace):
        return namespace.format_snake_case is True


class FormatCamelCase(FormatBase):
    def __init__(self):
        super().__init__(CaseDelimitedFormatter(CharacterType.LOWERCASE))

    def should_perform(self, namespace: Namespace):
        return namespace.format_camel_case is True

    def perform(self, namespace: Namespace):
        if namespace.format_literals:
            self._formatter = CaseDelimitedFormatter(CharacterType.LOWERCASE, namespace.format_literals)
        super().perform(namespace)


class FormatPascalCase(FormatBase):
    def __init__(self):
        super().__init__(CaseDelimitedFormatter(CharacterType.UPPERCASE))

    def should_perform(self, namespace: Namespace):
        return namespace.format_pascal_case is True

    def perform(self, namespace: Namespace):
        if namespace.format_literals:
            self._formatter = CaseDelimitedFormatter(CharacterType.UPPERCASE, namespace.format_literals)
        super().perform(namespace)


class FormatKebabCase(FormatBase):
    def __init__(self):
        super().__init__(CharacterDelimitedFormatter('-'))

    def should_perform(self, namespace: Namespace):
        return namespace.format_kebab_case is True


class FormatConstantCase(FormatBase):
    def __init__(self):
        super().__init__(CharacterDelimitedFormatter('_'))

    def should_perform(self, namespace: Namespace):
        return namespace.format_constant_case is True

    def perform(self, namespace: Namespace):
        formatter = self._formatter
        parsed_words = namespace.parsed_words
        formatted_strings = []

        for words in parsed_words:
            formatted_strings.append(formatter.format([CharacterContainer(str(word).upper()) for word in words]))

        namespace.formatted_strings = formatted_strings


class FormatDomain(FormatBase):
    def __init__(self):
        super().__init__(CharacterDelimitedFormatter('.'))

    def should_perform(self, namespace: Namespace):
        return namespace.format_domain is True


class FormatPath(FormatBase):
    def __init__(self):
        super().__init__(CharacterDelimitedFormatter('/'))

    def should_perform(self, namespace: Namespace):
        return namespace.format_path is True


class FormatCsv(FormatBase):
    def __init__(self):
        super().__init__(CharacterDelimitedFormatter(','))

    def should_perform(self, namespace: Namespace):
        return namespace.format_csv is True
