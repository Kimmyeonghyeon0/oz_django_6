from django.http import HttpRequest, HttpResponse
from ninja import Router, Schema
from pip._vendor.distro.distro import like

from tabom.models import Like
from tabom.services.like_service import do_like

router = Router()


class LikeRequest(Schema):
    user_id: int
    article_id: int


class LikeResponse(Schema):
    id: int
    user_id: int
    article_id: int


@router.post("/", response={201: LikeResponse})
def post_like(request: HttpRequest, like_request: LikeRequest) -> tuple[int, Like]:
    like = do_like(like_request.user_id, like_request.article_id)
    return 201, like
