from flask import Request, Response


def check_auth(env: str, db_password: str, request: Request) -> bool:
    if env == "production":
        pwd = request.args.get("pwd")
        if pwd != db_password:
            return False
        else:
            return True
    return True
