from os import getenv

ALL_EXTENSIONS = [
    "cogs.owner",
]

if getenv("dev") == 1:
    INITIAL_EXTENSIONS = [
        "cogs.owner",
        # "cogs.",
    ]
else:
    INITIAL_EXTENSIONS = ALL_EXTENSIONS
