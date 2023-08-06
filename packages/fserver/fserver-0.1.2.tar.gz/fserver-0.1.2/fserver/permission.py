from fserver import conf
from fserver.path_util import is_child
from fserver.path_util import normalize_path
from fserver.path_util import url_path_to_local_abspath


def path_permission_deny(path):
    """
    note that prior of block_list is high than one of allow_list,
    that is, even path is sub of allow_list, path will be denied if path is in block_list or block_list' sub path
    :param path:
    :return:
    """
    DENY = True
    ALLOW = not DENY
    if path == '' or path == '/' or path == 'favicon.ico':
        return ALLOW

    local_abspath = url_path_to_local_abspath(path)
    if not is_child(local_abspath, conf.ROOT) and local_abspath != conf.ROOT:
        return DENY

    if len(conf.BLOCK_LIST) == 0 and len(conf.ALLOW_LIST) == 0:  # disable allow or block list function
        return ALLOW

    np = normalize_path(path)
    if len(conf.ALLOW_LIST) > 0:  # allow_list mode
        if np in conf.ALLOW_LIST_PARENTS or np in conf.ALLOW_LIST:  # path is allow or parent of allow_list
            return ALLOW

        for w in conf.ALLOW_LIST:
            if is_child(np, w):
                for b in conf.BLOCK_LIST:
                    if is_child(np, b) or np == b:
                        return DENY
                return ALLOW  # path is child of allow_list and not child of block_list
        return DENY  # define ALLOW_LIST while path not satisfy ALLOW_LIST

    if len(conf.BLOCK_LIST) > 0:  # block_list mode
        for b in conf.BLOCK_LIST:
            if is_child(np, b) or np == b:
                return DENY  # path is in block_list
        return ALLOW
    return DENY
