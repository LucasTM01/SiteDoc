from __future__ import annotations

from fastapi import Request


def url_for(request: Request, path: str) -> str:
    return request.url_for(path)