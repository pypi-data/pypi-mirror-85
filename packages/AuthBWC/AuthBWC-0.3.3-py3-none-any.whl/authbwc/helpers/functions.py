from blazeutils.strings import randchars
from blazeweb.globals import settings
import six


def add_administrative_user(allow_profile_defaults=True):
    from getpass import getpass
    from compstack.auth.model.orm import User

    input_function = input
    if six.PY2:
        input_function = raw_input  # noqa

    defaults = settings.components.auth.admin
    # add a default administrative user
    if allow_profile_defaults and defaults.username and defaults.password and defaults.email:
        ulogin = defaults.username
        uemail = defaults.email
        p1 = defaults.password
    else:
        ulogin = input_function("User's Login id:\n> ")
        uemail = input_function("User's email:\n> ")
        while True:
            p1 = getpass("User's password:\n> ")
            p2 = getpass("confirm password:\n> ")
            if p1 == p2:
                break
    User.add_iu(
        login_id=six.text_type(ulogin),
        email_address=six.text_type(uemail),
        password=p1,
        super_user=True,
        reset_required=False,
        pass_reset_ok=False,
    )


def add_user(login_id, email, password=None, super_user=False, send_email=True):
    """
        Creates a new user and optionally sends out the welcome email
    """
    from compstack.auth.model.orm import User
    from compstack.auth.helpers import send_new_user_email

    u = User.add(
        login_id=login_id,
        email_address=email,
        password=password or randchars(8),
        super_user=super_user
    )
    if send_email:
        email_sent = send_new_user_email(u)
    else:
        email_sent = False
    return u, email_sent
