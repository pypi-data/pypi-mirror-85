"""Helper utility functions"""
import re
import typing
from pprint import pformat
from typing import Type, Any, List

import cutie
import typer
from halo import Halo

from mimosa import db
from mimosa.models import (
    SiteKeyLocation,
    SiteKeyUserLocation,
    TFirebaseDoc,
)


def company_name_from_email(email: str) -> str:
    """Return the first part of the domain name of an email as the company name."""
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if pattern.match(email) is None:
        raise ValueError(f"Not a valid email: {email}")

    email_parts = email.split("@")
    domain = email_parts[1]
    domain_parts = domain.split(".")
    company_name = domain_parts[0]
    return company_name


def convert_string_to_bool(user_input: str) -> bool:
    if user_input.lower() == "false":
        return False
    elif user_input.lower() == "true":
        return True
    else:
        raise ValueError(f"Could not convert '{user_input} to boolean")


def convert_string_to_none(user_input: str) -> None:
    if user_input.lower() != "none":
        raise ValueError(
            f"Could not convert {user_input} to None. Expected 'None' or 'none'."
        )
    return None


def prompt_site_key() -> str:
    return typer.prompt("For which site key?", type=str)


def choose_existing_company_id(site_key: str) -> str:
    if type(site_key) != str or len(site_key) == 0:
        raise ValueError("Expected site_key to be a non-empty string")
    spinner = Halo(text_color="blue")
    try:
        spinner.start("Fetching site key companies...")
        companies = db.query_all_site_key_companies(site_key)
        spinner.succeed()
    except db.NotFound as err:
        spinner.fail()
        raise err
    company_id_list = [f"{item[0]} ({item[1].get('name')})" for item in companies]
    typer.secho("Select company ID:", fg=typer.colors.CYAN)
    selected_index = cutie.select(company_id_list)
    return companies[selected_index][0]


def prompt(message: str, data_type=Type) -> Any:
    """More generic wrapper around typer.prompt"""
    return typer.prompt(message, type=data_type)


def check_site_key_exist(site_key: str):
    # Check if site key exists.
    spinner = Halo(text_color="blue")
    spinner.start(f"Checking if site key: {site_key} exists...")
    try:
        db.get_site_key(site_key)
        spinner.succeed()
    except (ValueError, db.NotFound) as err:
        spinner.fail()
        raise err


def site_locations_to_user_locations(
    loc_list: List[SiteKeyLocation], default_value: bool = True
) -> List[SiteKeyUserLocation]:
    ouptput_list: List[SiteKeyUserLocation] = []
    for loc in loc_list:
        sk_user_loc = SiteKeyUserLocation(key=loc.id, value=default_value, id=loc.id)
        errors = sk_user_loc.validate()
        if errors != {}:
            raise ValueError(f"loc: {sk_user_loc.id} {pformat(errors)}")

        ouptput_list.append(sk_user_loc)

    return ouptput_list


def prompt_to_fix(document: TFirebaseDoc) -> TFirebaseDoc:
    """
    Prompt the user to enter a new value for each invalid value on the document.

    Modifies document in place!
    """
    errors = document.validate()

    # A dictionary mapping the attribute names to the type hints.
    attribute_types = typing.get_type_hints(document)

    # If no errors return original document object.
    if errors == {}:
        return document

    while errors != {}:
        for key, value in errors.items():
            # Prompt for a new value.
            attribute_value = getattr(document, key)

            # For handling extraneous whitespace on phone numbers.
            if key == "phone":
                if type(attribute_value) is str:
                    setattr(document, key, attribute_value.strip())
                    # reassign updated value to variable for use in prompts.
                    attribute_value = getattr(document, key)

                    # re-check validation.
                    redo_errors = document.validate()
                    if "phone" not in redo_errors:
                        continue

            typer.secho(f"Previous value ({attribute_value}) for {key} was invalid.")
            data_type = attribute_types[key]
            if data_type not in [int, float, bool, str]:
                # todo: try/except data_type.__origin__ either list or dict parse with json.loads()
                raise TypeError(
                    f"Unable to parse a data type of {data_type} from the "
                    f"command line. This will need to be fixed in the "
                    f"database first."
                )

            new_value = prompt("Enter new value", data_type=data_type)

            # Set the attribute to the new value.
            setattr(document, key, new_value)

        # Re-validate the document.
        errors = document.validate()

    return document
