from os import getenv

ALL_EXTENSIONS = [
    "cogs.owner",
    "cogs.error",
    "cogs.help",
]

if getenv("DEV") == "1":
    INITIAL_EXTENSIONS = [
        "cogs.owner",
        "cogs.error",
        # "cogs.",
    ]
else:
    INITIAL_EXTENSIONS = ALL_EXTENSIONS
