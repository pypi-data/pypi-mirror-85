from abc import ABC, abstractmethod
from typing import List, Optional

from casec.container import CharacterType, CharacterContainer, Character


class ParserBase(ABC):
    def __init__(self, delimiter: CharacterType):
        self._delimiter = delimiter

    @property
    def delimiter(self) -> CharacterType:
        return self._delimiter

    def get_next_character(self, raw_container: CharacterContainer, index: int) -> Optional[Character]:
        next_character = None
        if index + 1 < len(raw_container.characters):
            next_character = raw_container.characters[index + 1]

        return next_character

    def get_previous_character(self, raw_container: CharacterContainer, index: int) -> Optional[Character]:
        previous_character = None
        if index - 1 >= 0:
            previous_character = raw_container.characters[index - 1]

        return previous_character

    @abstractmethod
    def parse(self, raw_container: CharacterContainer) -> List[CharacterContainer]:
        raise NotImplementedError


class CharacterDelimitedParser(ParserBase):
    def parse(self, raw_container: CharacterContainer) -> List[CharacterContainer]:
        delimiter = self._delimiter
        words = []
        index = 0
        container = CharacterContainer()
        while True:
            if index == len(raw_container.characters):
                break
            character: Character = raw_container.characters[index]
            previous_character = self.get_previous_character(raw_container, index)
            next_character = self.get_next_character(raw_container, index)
            if self._is_delimiter(character) and len(container.characters) > 0 and \
                    not self._is_delimiter(previous_character) and not self._is_delimiter(next_character):

                index += 1
                character = raw_container.characters[index]
                words.append(container)
                container = CharacterContainer()

            elif self._is_delimiter(previous_character) and not self._is_delimiter(character) \
                    and not self._is_delimiter(self.get_previous_character(raw_container, index - 1)):

                words.append(container)
                container = CharacterContainer()

            container.append_str(
                character.character.lower() if character.case == CharacterType.UPPERCASE else character.character
            )
            index += 1

        words.append(container)

        return words

    def _is_delimiter(self, character: Character):
        return character and character.case == self.delimiter


class CaseDelimitedParser(ParserBase):
    def __init__(self, delimiter: CharacterType, literals: List[str] = None):
        super().__init__(delimiter)
        self._have_words_started = False
        self._literals = literals or []

    @property
    def literals(self) -> List[str]:
        return self._literals

    @literals.setter
    def literals(self, literals: List[str]):
        self._literals = literals

    def parse(self, raw_container: CharacterContainer) -> List[CharacterContainer]:
        words = []
        index = 0
        self._have_words_started = False
        container = CharacterContainer()
        while True:
            if index == len(raw_container.characters):
                break
            character: Character = raw_container.characters[index]
            is_literal = False
            valid_literal = None
            for literal in self.literals:
                for i, c in enumerate(literal):
                    if i + index < len(raw_container.characters) and c == raw_container.characters[i + index].character:
                        is_literal = True

                    else:
                        is_literal = False
                        break

                if is_literal:
                    valid_literal = literal
                    break

            if self._has_seen_first_character(raw_container, index) \
                    and (self._is_new_word(raw_container, index) or
                         self._is_series_of_delimiters(raw_container, index)) \
                    and len(container.characters) > 0:

                words.append(container)
                container = CharacterContainer()

            if valid_literal:
                for c in valid_literal:
                    container.append_str(c.lower())
                    index += 1

                self._have_words_started = True
                if index < len(raw_container.characters):
                    words.append(container)
                    container = CharacterContainer()
                    character: Character = raw_container.characters[index]

                else:
                    break

            container.append_str(
                character.character.lower() if character.case == CharacterType.UPPERCASE else character.character
            )
            index += 1

        words.append(container)

        return words

    def _is_plural_series_of_delimiters(self, raw_container: CharacterContainer, index: int) -> bool:
        delimiter = self._delimiter
        previous_character = self.get_previous_character(raw_container, index)
        next_character = self.get_next_character(raw_container, index)
        two_characters_ahead = self.get_next_character(raw_container, index + 1)
        character: Character = raw_container.characters[index]

        return previous_character and previous_character.case == delimiter and character.case == delimiter \
            and next_character and next_character.character == 's' \
            and (not two_characters_ahead or two_characters_ahead.case == delimiter)

    def _is_new_word(self, raw_container: CharacterContainer, index: int):
        delimiter = self._delimiter
        normal_case = CharacterType.LOWERCASE if delimiter == CharacterType.UPPERCASE else CharacterType.UPPERCASE
        non_delimiters = [normal_case, CharacterType.DASH, CharacterType.DOT, CharacterType.UNDERSCORE,
                          CharacterType.SLASH, CharacterType.OTHER]
        previous_character = self.get_previous_character(raw_container, index)
        character: Character = raw_container.characters[index]

        return character.case == delimiter and previous_character and previous_character.case in non_delimiters

    def _is_series_of_delimiters(self, raw_container: CharacterContainer, index: int):
        delimiter = self._delimiter
        normal_case = CharacterType.LOWERCASE if delimiter == CharacterType.UPPERCASE else CharacterType.UPPERCASE
        next_character = self.get_next_character(raw_container, index)
        previous_character = self.get_previous_character(raw_container, index)
        character: Character = raw_container.characters[index]

        return previous_character and previous_character.case == delimiter and character.case == delimiter \
            and next_character and next_character.case == normal_case

    def _has_seen_first_character(self, raw_container: CharacterContainer, index: int):
        valid_first_characters = [
            CharacterType.UPPERCASE,
            CharacterType.LOWERCASE,
            CharacterType.OTHER
        ]
        have_words_started = self._have_words_started
        character = raw_container.characters[index]
        self._have_words_started = have_words_started or character.case in valid_first_characters

        return have_words_started
