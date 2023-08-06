from abc import ABC, abstractmethod
from typing import List

from casec.container import CharacterType, CharacterContainer


class FormatterBase(ABC):
    @abstractmethod
    def format(self, words: List[CharacterContainer]) -> str:
        raise NotImplementedError


class CaseDelimitedFormatter(FormatterBase):
    def __init__(self, first_character_casing: CharacterType, format_literals: List[str] = None):
        self._first_character_casing = first_character_casing
        self._format_literals = format_literals or []

    def format(self, words: List[CharacterContainer]) -> str:
        format_literals = [acronym.lower() for acronym in self._format_literals]
        case_delimited = CharacterContainer()
        first_character_casing = self._first_character_casing
        valid_first_characters = [
            CharacterType.UPPERCASE,
            CharacterType.LOWERCASE,
            CharacterType.OTHER
        ]
        should_capitalize = False
        is_first_word = True

        for word in words:
            if str(word) in format_literals:
                case_delimited.append_str(self._format_literals[format_literals.index(str(word))])
                is_first_word = False
                should_capitalize = True
            else:
                for character in word:
                    if is_first_word and character.case in valid_first_characters:
                        is_first_word = False
                        if first_character_casing == CharacterType.UPPERCASE:
                            case_delimited.append_str(character.character.upper())

                        elif first_character_casing == CharacterType.LOWERCASE:
                            case_delimited.append_str(character.character.lower())

                    elif should_capitalize:
                        case_delimited.append_str(character.character.upper())
                        should_capitalize = False

                    else:
                        case_delimited.append_str(character.character)

                should_capitalize = True and not is_first_word

        return str(case_delimited)


class CharacterDelimitedFormatter(FormatterBase):
    def __init__(self, delimiter: str):
        self._delimiter = delimiter

    def format(self, words: List[CharacterContainer]) -> str:
        return str(CharacterContainer(self._delimiter.join([str(w) for w in words])))
