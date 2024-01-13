def error(msg: str, exitf) -> None:
    result: None = None

    print(msg)
    exitf(0)

    return result