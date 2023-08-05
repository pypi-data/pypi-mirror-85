"""
Database migration code for Stilt 1 RTDB -> Stilt 2 Firestore.
"""
from enum import Enum
from typing import List

import typer
from halo import Halo

from mimosa.project import choose_project
from . import rtdb, db, utils, presets, user
from .models import (
    SiteKey,
    craft_type_codes,
    CraftTypes,
    task_type_codes,
    TaskTypes,
    task_status_codes,
    TaskStatus,
    event_type_codes,
    EventTypes,
    SiteKeyLocation,
    RootUserDoc,
    RootUserPrivateDoc,
    SiteKeyUser,
    SiteKeyUserPrivateDoc,
)
from .utils import prompt_to_fix

app = typer.Typer()


class RtdbURL(Enum):
    SCAFFOLD_TRACKER = "SCAFFOLD_TRACKER"
    STILT_DEV = "STILT_DEV"


project_database_urls = {
    RtdbURL.SCAFFOLD_TRACKER: "https://scaffoldtracker.firebaseio.com",
    RtdbURL.STILT_DEV: "https://stilt-dev.firebaseio.com",
}


@app.command(name="site-key")
def command_migrate_site_key(
    site_key: str,
    database_url: RtdbURL = typer.Argument(..., case_sensitive=False),
    all_types: bool = True,
    skip_project=False,
):
    """Migrate site key, site key locations, root users and site key users for a given
    site key."""
    migrate_site_key(site_key=site_key, database_url=database_url, all_types=all_types)
    typer.Exit()


def prompt_site_key_selection():
    pass


def migrate_site_key(
    site_key: str,
    database_url: RtdbURL,
    all_types: bool = True,
    skip_project: bool = False,
) -> None:
    """
    Convert a Stilt 1 Site Key to a Stilt 2 Site Key Document.

    Prompt to fix any errors. Enables all types by default.

    :param database_url:
    :param skip_project:
    :param site_key:
    :param all_types: Whether to enable all valid types or not.
    :return:
    """
    spinner = Halo(text_color="blue")
    choose_project(skip=skip_project, database_url=project_database_urls[database_url])

    try:
        spinner.start(f"Checking if {site_key} exists...")
        db.get_site_key(site_key)
        spinner.succeed()
        site_key_exists = True
    except db.NotFound as err:
        spinner.succeed()
        site_key_exists = False

    if site_key_exists:
        typer.secho(f"Site key {site_key} exists. Skipping.")

    else:
        spinner.start(f"Fetching name for {site_key}...")
        try:
            name = rtdb.read_site_key_name(site_key)
            spinner.succeed()
        except Exception as err:
            spinner.fail()
            raise err
        spinner.start(f"Fetching timezone for {site_key}...")
        try:
            timezone = rtdb.read_site_key_timezone(site_key)
            spinner.succeed()
        except Exception as err:
            spinner.fail()
            raise err

        old_site_key_data = {"name": name, "timezone": timezone}
        new_site_key = convert_site_key(old_site_key_data, all_types=all_types)
        new_site_key = prompt_to_fix(new_site_key)

        db.set_site_key(site_key, new_site_key.to_firestore())

    # Continue with migrating site locations.
    migrate_site_locations(site_key=site_key)

    # Create server user
    user.create_server_user(site_key=site_key)

    # Migrate users in site key
    migrate_site_users(site_key=site_key)

    return


def migrate_site_locations(site_key: str) -> None:
    """
    Migrate site location data from Stilt 1's Real-time Database to Stilt 2's
    Firestore database.
    """

    spinner = Halo(text_color="blue")

    # Read all locations from RTDB.
    locations = rtdb.read_all_site_key_locations(site_key=site_key)

    if locations is None:
        typer.secho(f"No locations found for {site_key}", fg="red", bold=True)
        return

    # Perform read, convert, validation, and write for each location.
    for location_id, location_data in locations.items():

        # Check if location already exists in Firestore.
        try:
            spinner.start(f"Checking if location {location_id} exists...")
            db.get_site_key_location(site_key, location_id)
            spinner.info(f"Location {location_id} already exists. Skipping.")
            location_exists = True
        except db.NotFound as err:
            spinner.succeed()
            location_exists = False

        # If location already exists in Firestore, skip write and continue to next
        # item in dictionary.
        if location_exists:
            continue

        # Convert to Stilt 2 schema.
        new_location = convert_site_key_location(location_data)
        # Prompt user to fix any errors.
        new_location = prompt_to_fix(new_location)

        # Write data to Firestore.
        spinner.start(f"Writing location {location_id}...")
        try:
            db.set_site_key_location(
                site_key=site_key,
                location_id=location_id,
                updates=new_location.to_firestore(),
            )
            spinner.succeed()
        except Exception as err:
            spinner.fail()
            raise err

    typer.secho(
        f"Migration complete for {site_key}! You did good. Real good.",
        fg="green",
        bold=True,
    )

    return


def migrate_site_users(site_key: str) -> None:
    """
    Migrate root and site key user data from Stilt 1 to Stilt 2 Firestore.

    Based on UIDs in the site key users node.
    """

    spinner = Halo(text_color="blue")

    # Read user data from RTDB site key
    rtdb_site_key_users = rtdb.read_all_site_key_users(site_key)

    if rtdb_site_key_users is None:
        typer.secho(f"No site key users found for {site_key}", fg="red", bold=True)
        return

    # Query for all the locations that exist on the site key.
    site_locations = db.query_all_site_locations(site_key=site_key)

    if len(site_locations) == 0:
        typer.secho(
            f"No locations found for {site_key}. Is this a valid site key?",
            bold=True,
            fg="red",
        )

    # For each user, migrate a root user document.
    for uid, user_data in rtdb_site_key_users.items():

        # Initialize new_root_user_doc so we can check to reuse it for new site
        # key user
        new_root_user_doc = None

        # Check if root user already exists in Firestore.
        try:
            spinner.start(f"Checking if root user {uid} exists...")
            db.get_root_user(uid=uid)
            spinner.info(f"Root user {uid} already exists. Skipping.")
            root_user_exists = True
        except db.NotFound as err:
            spinner.succeed()
            root_user_exists = False

        # If the root user doesn't exist in Firestore, perform conversion and set/write
        # operations.
        if not root_user_exists:
            # Convert to Firestore root user document.
            new_root_user_doc = convert_site_key_user_to_root_user(user_data)
            new_root_user_doc = prompt_to_fix(new_root_user_doc)

            # Validate the private data document
            new_private_doc = RootUserPrivateDoc({f"{site_key}": False})
            private_doc_errors = new_private_doc.validate()
            if private_doc_errors != {}:
                typer.secho(
                    f"Skipping write. Error validating the root user private doc. {private_doc_errors}",
                    fg="red",
                    bold=True,
                )
                continue

            spinner.start(f"Writing root user doc {uid}...")
            try:
                # Write root user doc
                db.set_root_user(uid=uid, updates=new_root_user_doc.to_firestore())
                spinner.succeed()

            except Exception as err:
                spinner.fail()
                raise err

            spinner.start(f"Writing root user private doc for {uid}...")
            try:
                # Write private doc
                db.set_root_user_permissions(
                    uid=uid, updates=new_private_doc.to_firestore()
                )
                spinner.succeed()

            except Exception as err:
                spinner.fail()
                raise err

        # Migrate/generate a site key user document.

        # Check if site key user already exists in Firestore.
        try:
            spinner.start(f"Checking if user {uid} exists for {site_key}...")
            db.get_sk_user(site_key=site_key, uid=uid)
            spinner.info(f"User {uid} already exists for {site_key}. Skipping.")
            sk_user_exists = True
        except db.NotFound as err:
            spinner.succeed()
            sk_user_exists = False

        # If the site key user doesn't exist in Firestore, perform conversion and
        # set/write operations.
        if not sk_user_exists:

            # Convert to Stilt 2 Site Key User from Stilt 1 RTDB Site Key user data or
            # from the previously created new_root_user_doc.
            # Add 'empty' permissions document as default.
            if type(new_root_user_doc) is RootUserDoc:
                new_site_key_user = convert_site_key_user(
                    new_root_user_doc.to_firestore()
                )
            else:
                new_site_key_user = convert_site_key_user(user_data)

            new_site_key_user = prompt_to_fix(new_site_key_user)

            all_false_permissions = presets.user_perm_presets[
                presets.UserPresets.ALL_FALSE
            ]
            new_user_permissions_doc = SiteKeyUserPrivateDoc(**all_false_permissions)
            new_user_permissions_doc = prompt_to_fix(new_user_permissions_doc)

            # Write site key user.
            try:
                spinner.start(f"Writing site key user data for {uid}...")
                db.set_site_key_user(
                    site_key=site_key, uid=uid, updates=new_site_key_user.to_firestore()
                )
                spinner.succeed()
            except Exception as err:
                spinner.fail()
                raise err

            # Write site key user privateDoc
            try:
                spinner.start(f"Writing site key user private data for {uid}...")
                db.set_site_key_user_private_data(
                    site_key=site_key,
                    uid=uid,
                    updates=new_user_permissions_doc.to_firestore(),
                )
                spinner.succeed()
            except Exception as err:
                spinner.fail()
                raise err

        # Write site key user default locations.
        user.update_site_key_user_locations(
            site_key=site_key,
            site_locations=site_locations,
            uid=uid,
            stilt_one_user_locations=user_data.get("locations"),
        )

        typer.secho(f"Migration for user {uid} finished.", fg="green", bold=True)

    return


def convert_site_key(old_data: dict, all_types: bool = True) -> SiteKey:
    """Convert Stilt 1 site key data into a Stilt 2 Firestore site key document."""
    # Add all valid types.
    if all_types:
        valid_craft_types: List[int] = [craft_type_codes[e] for e in list(CraftTypes)]
        valid_task_types: List[int] = [task_type_codes[e] for e in list(TaskTypes)]
        valid_task_status_codes: List[int] = [
            task_status_codes[e] for e in list(TaskStatus)
        ]
        valid_event_types: List[int] = [event_type_codes[e] for e in list(EventTypes)]

    # Default to empty list for valid types.
    else:
        valid_craft_types = []
        valid_task_types = []
        valid_task_status_codes = []
        valid_event_types = []

    return SiteKey(
        name=old_data.get("name"),
        timezone=old_data.get("timezone"),
        managingCompanyID="",  # use empty string for now.
        unapprovedUsers=[],
        validCraftTypes=valid_craft_types,
        validTaskTypes=valid_task_types,
        validTaskStatusCodes=valid_task_status_codes,
        validEventTypes=valid_event_types,
        customizations={},
    )


def convert_site_key_location(old_data: dict) -> SiteKeyLocation:
    """Convert Stilt 1 site location data to Stilt 2 Document."""
    return SiteKeyLocation(
        department=old_data.get("department"),
        title=old_data.get("title"),
        latitude=old_data.get("latitude"),
        longitude=old_data.get("longitude"),
    )


def convert_site_key_user(old_data: dict, company_name: str = None) -> SiteKeyUser:
    """
    Create a Stilt 2 SiteKeyUser document from Stilt 1 site key user data.

    Uses the passed in company name value since there is not an equivalent on the RTDB
    site key user node.
    """
    return SiteKeyUser(
        displayName=old_data.get("displayName"),
        companyName=utils.company_name_from_email(old_data.get("email")),
        jobTitle=old_data.get("jobTitle"),
        email=old_data.get("email"),
        department=old_data.get("department"),
        phone=old_data.get("phone"),
    )


def convert_site_key_user_to_root_user(old_data: dict) -> RootUserDoc:
    """Create a Stilt 2 RootUserDoc from Stilt 1 site key user data."""
    return RootUserDoc(
        displayName=old_data.get("displayName"),
        companyName=utils.company_name_from_email(old_data.get("email")),
        jobTitle=old_data.get("jobTitle"),
        department=old_data.get("department"),
        phone=old_data.get("phone"),
        receiveNotifications=True,
        email=old_data.get("email"),
    )


def main():
    app()


if __name__ == "__main__":
    main()
