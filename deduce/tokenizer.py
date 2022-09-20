""" This module contains all tokenizing functionality """
import itertools
from enum import Enum, auto
from typing import Iterable

import docdeid
import docdeid.tokenizer.tokenizer
from docdeid.datastructures.lookup import LookupTrie


class _CharType(Enum):

    ALPHA = auto()
    OTHER = auto()


class Tokenizer(docdeid.BaseTokenizer):
    def __init__(self, merge_terms: Iterable = None):

        self._trie = None

        if merge_terms is not None:
            self._trie = LookupTrie()

            for term in merge_terms:
                tokens = [token.text for token in self.tokenize(text=term, merge=False)]
                self._trie.add(tokens)

    @staticmethod
    def _character_type(char: str) -> _CharType:

        if char.isalpha():
            return _CharType.ALPHA

        return _CharType.OTHER

    def _merge_triebased(self, tokens: list[docdeid.Token]) -> list[docdeid.Token]:

        tokens_text = [token.text for token in tokens]
        tokens_merged = []
        i = 0

        while i < len(tokens):

            longest_matching_prefix = self._trie.longest_matching_prefix(
                tokens_text[i:]
            )

            if longest_matching_prefix is None:
                tokens_merged.append(tokens[i])
                i += 1

            else:
                num_tokens_to_merge = len(longest_matching_prefix)
                tokens_merged.append(
                    self.join_tokens(tokens[i : i + num_tokens_to_merge])
                )
                i += num_tokens_to_merge

        return tokens_merged

    @staticmethod
    def join_tokens(tokens: list[docdeid.Token]):

        return docdeid.Token(
            text="".join(token.text for token in tokens),
            start_char=tokens[0].start_char,
            end_char=tokens[-1].end_char,
            index=tokens[0].index,
        )

    def tokenize(
        self, text: str, merge: bool = True) -> list[docdeid.Token]:

        if merge and self._trie is None:
            raise AttributeError(
                "Trying to use the tokenize with merging, but no merge terms specified."
            )

        tokens = []
        last_split = 0

        # Iterate over all chars in the text
        for index, char in enumerate(text):

            if index == 0:
                continue

            # Split if we transition between character types
            if self._character_type(char) != self._character_type(text[index - 1]):
                tokens.append(
                    docdeid.Token(
                        start_char=last_split,
                        end_char=index,
                        text=text[last_split:index],
                        index=0,
                    )
                )
                last_split = index

        # Append the tokens
        tokens.append(
            docdeid.Token(
                start_char=last_split,
                end_char=len(text),
                text=text[last_split:],
                index=0,
            )
        )

        if merge:
            tokens = self._merge_triebased(tokens)

        return [
            docdeid.Token(
                text=token.text,
                start_char=token.start_char,
                end_char=token.end_char,
                index=i,
            )
            for token, i in zip(tokens, itertools.count())
        ]
