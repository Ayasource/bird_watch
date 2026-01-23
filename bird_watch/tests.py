from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Bird, Entry
from .forms import BirdForm

class BirdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.bird = Bird.objects.create(
            bird_name='Blue Tit',
            created_by=self.user,
            bird_count=2,
            status=1
        )

    def test_bird_creation(self):
        self.assertEqual(self.bird.bird_name, 'Blue Tit')
        self.assertEqual(self.bird.bird_count, 2)
        self.assertEqual(self.bird.created_by.username, 'testuser')

    def test_bird_str_method(self):
        expected = f"testuser saw 2 Blue Tit(s) on {self.bird.date.strftime('%Y-%m-%d')}"
        self.assertEqual(str(self.bird), expected)


class BirdViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.bird = Bird.objects.create(
            bird_name='Robin',
            created_by=self.user,
            bird_count=1,
            status=1
        )

    def test_add_bird_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('add_bird'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bird_watch_post/add_bird.html')

    def test_add_bird_view_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_bird'), {
            'bird_name': 'Sparrow',
            'bird_count': 3,
            'status': 1
        }, follow=True)  # Follow the redirect
        self.assertEqual(Bird.objects.count(), 2)
        self.assertTrue(Bird.objects.filter(bird_name='Sparrow').exists())
        self.assertEqual(Bird.objects.get(bird_name='Sparrow').bird_count, 3)

    def test_bird_entry_requires_login(self):
        response = self.client.get(reverse('bird_entry', args=[self.bird.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_user_bird_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('bird_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Robin')


class BirdFormTest(TestCase):
    def test_bird_form_valid_data(self):
        form = BirdForm(data={
            'bird_name': 'Woodpecker',
            'bird_count': 1,
            'status': 1
        })
        self.assertTrue(form.is_valid())

    def test_bird_form_invalid_data(self):
        form = BirdForm(data={
            'bird_name': '',
            'bird_count': 1,
            'status': 1
        })
        self.assertFalse(form.is_valid())
