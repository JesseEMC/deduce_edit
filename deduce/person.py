from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union
from datetime import datetime


@dataclass
class Person:
    """
    Contains information on a person.

    Usable in a document metadata, where annotators can access it for annotation.
    """

    first_names: Optional[list[str]] = None
    initials: Optional[str] = None
    surname: Optional[str] = None
    birth_date: Optional[Union[datetime, str]] = None

    def __post_init__(self):
        if isinstance(self.birth_date, str):
            try:
                self.birth_date = datetime.strptime(self.birth_date, "%d-%m-%Y")
            except ValueError:
                raise ValueError("Birth date format should be DD-MM-YYYY")

    @classmethod
    def from_keywords(
        cls,
        patient_first_names: str = "",
        patient_initials: str = "",
        patient_surname: str = "",
        patient_given_name: str = "",
        patient_birth_date: str = "",
    ) -> Person:
        """
        Get a Person from keywords. Mainly used for compatibility with keyword as used
        in deduce<=1.0.8.

        Args:
            patient_first_names: The patient first names, separated by whitespace.
            patient_initials: The patient initials.
            patient_surname: The patient surname.
            patient_given_name: The patient given name.

        Returns:
            A Person object containing the patient information.
        """

        patient_first_names_lst = []

        if patient_first_names:
            patient_first_names_lst = patient_first_names.split(" ")

        if patient_given_name:
            patient_first_names_lst.append(patient_given_name)

        return cls(
            first_names=patient_first_names_lst or None,
            initials=patient_initials or None,
            surname=patient_surname or None,
            birth_date=patient_birth_date or None,
        )
