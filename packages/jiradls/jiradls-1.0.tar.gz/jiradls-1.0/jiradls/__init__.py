__version__ = "1.0"


def jiradls():
    # Shortcut to create a Diamond JIRA object.
    import jiradls.dlsjira

    return jiradls.dlsjira.DLSJIRA()
