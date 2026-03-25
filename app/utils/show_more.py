"""
Utilitaire « Afficher plus » — pagination progressive réutilisable.

Logique :
    Étape 0  → affiche `initial` éléments           (ex. 5)
    Étape 1  → affiche initial + steps[0]            (ex. 5+10 = 15)
    Étape 2  → affiche initial + steps[0] + steps[1] (ex. 5+10+20 = 35)
    Étape N  → si steps[N-1] == -1 → affiche tout

Les paliers sont cumulatifs.  Le dernier palier devrait toujours être -1
pour garantir qu'on puisse tout afficher.

Usage dans une route Flask :
    from app.utils.show_more import paginate_show_more

    result = paginate_show_more(
        items     = all_students,          # liste complète (déjà triée)
        more      = request.args.get("more", 0, type=int),
        initial   = app.config["PROFILE_LIST_INITIAL"],   # 5
        steps     = app.config["PROFILE_LIST_STEPS"],      # [10, 20, -1]
    )
    # result = {"items": [...], "total": 30, "has_more": True, "next_more": 2}
"""


def paginate_show_more(items, more=0, initial=5, steps=None):
    """Renvoie un dict avec les éléments à afficher et les métadonnées.

    Paramètres
    ----------
    items : list
        Liste complète des éléments (déjà triée côté appelant).
    more : int
        Palier courant issu du query-string ``?more=``.  0 = première visite.
    initial : int
        Nombre d'éléments affichés au chargement initial (palier 0).
    steps : list[int]
        Incréments successifs.  ``-1`` = « tout afficher ».
        Défaut : ``[10, 20, -1]``.

    Retour
    ------
    dict  ``{"items", "total", "has_more", "next_more"}``
    """
    if steps is None:
        steps = [10, 20, -1]

    total = len(items)

    # Calcul de la limite cumulative
    limit = initial
    for i in range(min(more, len(steps))):
        if steps[i] == -1:
            limit = total
            break
        limit += steps[i]

    # Si le palier courant pointe directement sur -1
    if more > 0 and more <= len(steps) and steps[min(more, len(steps)) - 1] == -1:
        limit = total

    show_all = limit >= total
    displayed = items if show_all else items[:limit]

    # Prochain palier
    if show_all:
        has_more = False
        next_more = None
    else:
        has_more = True
        next_more = more + 1 if more < len(steps) else None

    return {
        "items":     displayed,
        "total":     total,
        "has_more":  has_more,
        "next_more": next_more,
    }
