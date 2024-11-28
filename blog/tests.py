from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Post

class PostTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_delete_post(self):
        post = Post.objects.create(
            title='Test Post to delete',
            content='This post will be deleted.',
            author=self.user,
            created_at=timezone.now()
        )
        url = reverse('home')
        response = self.client.post(url, {'post_id': post.id, 'action': 'delete_post'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_post_forbidden(self):
        other_user = get_user_model().objects.create_user(
            username='otheruser', password='password'
        )
        post = Post.objects.create(
            title='Test Post to delete by another user',
            content='This post will be deleted by another user.',
            author=self.user,
            created_at=timezone.now()
        )
        self.client.login(username='otheruser', password='password')
        url = reverse('home')
        response = self.client.post(url, {'post_id': post.id, 'action': 'delete_post'})
        self.assertEqual(response.status_code, 403)

    def test_login_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_edit_post_view(self):
        post = Post.objects.create(
            title='Test Post for Editing',
            content='Content before edit.',
            author=self.user,
            created_at=timezone.now()
        )
        url = reverse('edit_post', args=[post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_post.html')

        updated_data = {'title': 'Updated Test Post', 'content': 'Updated content.'}
        response = self.client.post(url, updated_data)
        post.refresh_from_db()
        self.assertEqual(post.title, 'Updated Test Post')
        self.assertEqual(post.content, 'Updated content.')

    def test_edit_post_forbidden(self):
        other_user = get_user_model().objects.create_user(
            username='otheruser', password='password'
        )
        post = Post.objects.create(
            title='Test Post for Editing',
            content='Content before edit.',
            author=self.user,
            created_at=timezone.now()
        )
        self.client.login(username='otheruser', password='password')
        url = reverse('edit_post', args=[post.id])
        response = self.client.post(url, {'title': 'Other User Post Edit', 'content': 'This should not work.'})
        self.assertEqual(response.status_code, 403)

    def test_logout_view_redirects_to_home(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('logout')
        response = self.client.post(url)

        self.assertRedirects(response, reverse('home'))
