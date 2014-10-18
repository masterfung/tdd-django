from django.core.urlresolvers import resolve
from django.test import TestCase
from .views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

# Create your tests here.
from .models import Item


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item EVER'
        first_item.save()

        second_item = Item()
        second_item.text = 'Second thing on the agenda'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item EVER')
        self.assertEqual(second_saved_item.text, 'Second thing on the agenda')


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_views(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-best/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response = self.client.get('/lists/the-best/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST_success(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        self.assertRedirects(response, '/lists/the-best/')