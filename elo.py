R0 = 1500
K0 = 40
K = 20

def K_inter(_c):
    return K + (1 / _c) * K


def compute_estimated(r_a, r_b):
    return 1. / (1. + 10**((r_b - r_a) / 400))


def compute_new_rating(r_a, k, win, e_a):
    _w = 1 if win else 0
    return r_a + k * (_w - e_a)


def update_elo(ida, idb, relations, win):
    """
    Returns a ELO update query for a user.

    :param ida: Id of user A
    :param idb: Id of user B
    :param relations: Dict of relations 
    :param win: True if A won, False if B won
    :return: Update query :3
    """

    _rating_a, _rating_b = R0, R0
    _count_a, _count_b = 1, 1

    if ida not in relations.keys():
        relations[ida] = {"count": 1, "elo": _rating_a}
    else:
        relations[ida]["count"] += 1
        _rating_a = relations[ida]["elo"]
        _count_a = relations[ida]["count"]

    if idb not in relations.keys():
        relations[idb] = {"count": 1, "elo": _rating_b}
    else:
        relations[idb]["count"] += 1
        _rating_b = relations[idb]["elo"]
        _count_b = relations[idb]["count"]

    _computed_a = compute_estimated(_rating_a, _rating_b)
    _new_rating_a = compute_new_rating(
        _rating_a, 
        K_inter(_count_a), 
        win, 
        _computed_a)

    _computed_b = compute_estimated(_rating_b, _rating_a)
    _new_rating_b = compute_new_rating(
        _rating_b,
        K_inter(_count_b), 
        not win,
        _computed_b)

    relations[ida]["elo"] = _new_rating_a
    relations[idb]["elo"] = _new_rating_b

    return {"$set": {"relations": relations}}

if __name__ == "__main__":
    _ida, _idb = "1", "2"
    _rel = {
        "1": {"count": 1, "elo": 1789},
        "2": {"count": 1, "elo": 1689},
    }

    _new_rel = update_elo(_ida, _idb, _rel, False)
    print(_new_rel)
