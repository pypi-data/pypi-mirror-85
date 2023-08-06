def make_request_account_id(account_id: str) -> str:
    """ Removes '-' from account_id to make it valid for requests """
    return account_id.replace('-', '')
