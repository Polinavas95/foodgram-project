import re

import pytest
from django.test import Client, TestCase

from recipes.models import Recipe
from users.models import User


class TestFavorite(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@.com', password='1234567')
        self.user2 = User.objects.create_user(username='user2', email='user2@.com', password='123456')
        self.recipe1 = Recipe.objects.create(author=self.user1, duration=10, title='title1', text='text1')
        self.recipe2 = Recipe.objects.create(author=self.user2, duration=10, title='title2', text='text2')

    def test_follow_favorite(self):
        response = self.client.post('/api/favorites/', {'id': 1})
        assert response.status_code == 403, 'Незалогиненный пользователь не может добавить рецепт в избранное'
        self.client.login(username='user1', password='1234567')
        response = self.client.post('/api/favorites/', {"id": 2})
        assert response.status_code == 200, 'Залогиненный пользователь может добавить чужой рецепт в избранное'
        assert response.data == {'success': True}, 'При успешном добавлении возвращается "True"'
        response = self.client.post('/api/favorites/', {'id': 2})
        assert response.status_code == 200, 'Залогиненный пользователь может добавить чужой рецепт в избранное'
        assert response.data == {'success': False}, 'Пользователь не может повторно добавить рецепт в избранное'
        response = self.client.post('/api/favorites/', {'id': 1})
        assert response.data == {'success': False}, 'Пользователь не может добавить в избранное свой рецепт'

    def test_unfollow_favorite(self):
        self.client.login(username='user1', password='1234567')
        self.client.post('/api/favorites/', {'id': 2})
        assert self.user1.favorites.count() == 1, 'Проверьте, что вы подписаны'
        self.client.delete('/api/favorites/2/')
        assert self.user1.favorites.count() == 0, 'Проверьте, что вы отписались'
