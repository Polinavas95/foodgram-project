from django.test import Client, TestCase

from recipes.models import Recipe
from users.models import User


class TestPurchase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@.com', password='1234567')
        self.user2 = User.objects.create_user(username='user2', email='user2@user2.com', password='123456')
        self.recipe1 = Recipe.objects.create(author=self.user1, duration=10, title='title1', text='text1')
        self.recipe2 = Recipe.objects.create(author=self.user2, duration=10, title='title2', text='text1')

    def test_add_to_purchase(self):
        response = self.client.post('/api/purchases/')
        assert response.status_code == 403, 'Незалогиненный пользователь не может добавить рецепт в покупки'
        self.client.login(username='user1', password='1234567')
        response = self.client.post('/api/purchases/', {'id': 2})
        assert response.status_code == 200, 'Залогиненный пользователь может добавить рецепт в покупки'
        assert response.data == {'success': True}, 'При успешном добавлении возвращается True'
        response = self.client.post('/api/purchases/', {'id': 2})
        assert response.status_code == 200, 'Залогиненный пользователь может добавить рецепт в покупки'
        assert response.data == {'success': False}, 'Пользователь не может повторно добавить рецепт в покупки'
        response = self.client.post('/api/purchases/', {'id': 1})
        assert response.data == {'success': True}, 'Пользователь может добавить в покупки свой рецепт'

    def test_remove_to_purchase(self):
        self.client.login(username='user1', password='1234567')
        self.client.post('/api/purchases/', {'id': 2})
        assert self.user1.purchases.count() == 1, 'Проверьте, что вы подписаны'
        self.client.delete('/api/purchases/2/')
        assert self.user1.purchases.count() == 0, 'Проверьте, что вы отписались'