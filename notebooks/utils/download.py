import os
import requests
import json
import urllib3


def get_api_key() -> str:
    """Read `.api_key` file in the current directory and return the api key.

    User needs to add `.api_key` in the current directory with api key. If it is
    not present then it will return an empty string.

    Returns
    -------
    str
        api key.
    """

    api_key_path = os.path.join(os.path.dirname(__file__), ".api_key")
    if not os.path.exists(api_key_path):
        return ""

    with open(api_key_path, "r") as reader:
        return reader.read()


def download_3d_similar_molecules(query_smiles: str, save_path: str) -> bool:
    """Download 3d similar molecules using cheese api.

    Make sure that download directory exists.

    Parameters
    ----------
    query_smiles : str
        query molecule smiles
    save_path : str
        path to save the downloaded file.

    Returns
    -------
    bool
        True if downloaded successfully.
    """

    api_key = get_api_key()

    if api_key == "":
        print("Unable to get api key.")
        return False

    if not os.path.exists(os.path.dirname(save_path)):
        print("Directory doesn't exist.")
        return False

    search_types = ['morgan', 'espsim_electrostatic', 'espsim_shape', 'consensus']
    responses = []

    try:
        urllib3.disable_warnings()
        for search_type in search_types:
            res = requests.get(
                "https://api.cheese.themama.ai/molsearch",
                {
                    "search_input": query_smiles,
                    "search_type": search_type,
                    "n_neighbors": 100,
                    "search_quality": "very accurate",
                    "descriptors": False,
                    "properties": False,
                    "filter_molecules": False,
                },
                headers={"Authorization": f"Bearer {api_key}"},
                verify=False,
            ).json()

            responses.extend(res['neighbors'])

    except Exception as e:
        print(e)
        return False
    
    with open(save_path, "w") as writer:
        json.dump(responses, writer, indent=2)
    return True
