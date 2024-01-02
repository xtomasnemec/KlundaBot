characters = [
    # Hoisted characters
    ["silver", "Silver", None],
    ["barry", "Barry", None],
    # The rest is ordered alphabetically
    ["amy", "Amy", None],
    ["bean", "Bean", None],
    ["blaze", "Blaze", None],
    ["cream", "Cream", None],
    ["eggman", "Eggman", None],
    ["gamma", "Gamma", None],
    ["lanolin", "Lanolin", None],
    ["quickstrike", "Quickstrike", "@shadzydow's Original Character. Added on request."],
    ["ray", "Ray", None],
    ["shadow", "Shadow", None],
    ["sharp", "Sharp", "@thesupershotgun's Original Character. Added on request."],
    ["sonic", "Sonic", None],
    ["tails", "Tails", None],
    ["tangle", "Tangle", None],
    ["vector", "Vector", None],
    ["whisper", "Whisper", None],
]

def get_list():
    l = []
    for c in characters:
        l.append(c[1])
    return l
