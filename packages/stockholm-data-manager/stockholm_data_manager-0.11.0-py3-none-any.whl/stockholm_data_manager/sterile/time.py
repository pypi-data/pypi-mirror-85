import time


def sleep(n: int, env: str = "test") -> None:
    if env == "test":
        return None
    time.sleep(n)
