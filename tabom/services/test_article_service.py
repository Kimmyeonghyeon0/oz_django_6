from audioop import reverse

from django.test import TestCase

from tabom.models import Article, Like, User
from tabom.services.article_service import get_an_article, get_article_list
from tabom.services.like_service import do_like


class TestArticleService(TestCase):
    def test_you_can_get_an_article_by_id(self) -> None:
        # Given
        title = "test_title"
        article = Article.objects.create(title=title)

        # When
        result_article = get_an_article(article.id)

        # Then
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_exception_when_article_does_not_exist(self) -> None:
        # Given
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(Article.DoesNotExist):
            get_an_article(invalid_article_id)

    def test_get_article_list_should_prefetch_likes(self) -> None:
        # Given
        user = User.objects.create(name="user1")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]
        Like.objects.create(user_id=user.id, article_id=articles[-1].id)

        # When
        # result_articles = get_article_list(0, 10)

        # Then
        with self.assertNumQueries():
            result_articles = get_article_list(0, 10)
            result_count = [a.like_set.count() for a in result_articles]

            self.assertEqual(len(result_articles), 10)
            self.assertEqual(1, result_count[0])
            self.assertEqual([a.id for a in reversed(articles[10:21])], [a.id for a in result_articles])

    def test_get_article_list_should_prefetch_like(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]
        do_like(user.id, articles[-1].id)
