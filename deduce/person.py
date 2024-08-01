rom __future__ import annotations

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
    birth_date: Optional[datetime] = None

    def __init__(
        self,
        first_names: Optional[list[str]] = None,
        initials: Optional[str] = None,
        surname: Optional[str] = None,
        birth_date: Optional[Union[datetime, str]] = None,
    ):
        self.first_names = first_names
        self.initials = initials
        self.surname = surname
        if isinstance(birth_date, str):
            self.birth_date = datetime.strptime(birth_date, "%d-%m-%Y")
        else:
            self.birth_date = birth_date

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
            patient_birth_date: The patient's birth date in the format "DD-MM-YYYY".

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

# Example usage
patient = Person(first_names=["wakuwaku"], initials="JJ", surname="Blrg", birth_date="11-03-1998")

# Assuming `deduce` is a module and `deidentify` is a function within it
doc = deduce.deidentify(text, metadata={'patient': patient})

# Print the deidentified text
print(doc.deidentified_text)
