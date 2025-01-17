import hashlib
import json
import os
import urllib

import sabath


def hashable(dct):
    "Create hashable string by  normalizing a JSON-serializable dictionary"
    # return the same dictionary with sorted keys
    return json.dumps({k: dct[k] for k in sorted(dct.keys())})

def cache_path(name, kind):
    dgst = hashlib.sha256(name.encode()).hexdigest()
    return os.path.join(sabath.cache, dgst[:2], dgst[2:], kind)

def get_fragment_cache_path(fragment, create=False):
    cchpth = cache_path(fragment["url"], "url")
    if create:
        os.makedirs(cchpth, exist_ok=True)

    base, fname = os.path.split(fragment["url"])
    return cchpth, fname

def get_model_repo_cache_path(model, create=False):
    cchpth = cache_path(hashable(model["git"]), "git")
    if create:
        os.makedirs(cchpth, exist_ok=True)

    repo = os.path.split(os.path.splitext(urllib.parse.urlparse(model["git"]["origin"]).path)[0])[-1]
    return cchpth, repo