import os


def get_api_key() -> str:
    """Read .`api_key` file in the current directory and return the api key.

    User needs to add `.api_key` in the current directory with api key. If it is
    not present then it will return an empty string.

    Returns
    -------
    str
        api key.
    """

    api_key_path = os.path.join(".", ".api_key")

    if not os.path.exists(api_key_path):
        return ""

    with open(api_key_path, "r") as reader:
        return reader.read()
