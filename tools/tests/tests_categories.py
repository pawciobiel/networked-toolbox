from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile

from common.testlib import TEST_PNG_CONTENT
from ..models import Tool, ToolCategory, CategoryGroup


class CategoriesViewsTestCase(TestCase):

    def setUp(self):
        self.test_admin = User.objects.create(username='testadmin')
        self.test_admin.set_password('testpass')
        self.admins_group = Group.objects.get(name='admins')
        self.test_admin.groups.add(self.admins_group)
        self.test_admin.save()

        self.test_category = ToolCategory.objects.create(
            title='test cat',
            description='test cat description'
        )
        self.test_tool = Tool.objects.create(
            title='test cat',
            description='test cat description'
        )
        self.test_tool.categories.add(self.test_category)

    def test_list_categories_get(self):
        resp = self.client.get(reverse('tools:list_categories'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/list_categories.html')
        self.assertContains(resp, 'Toolbox Overview')
        self.assertNotContains(resp, 'Add Group')
        self.assertNotContains(resp, 'Unpublished')

    def test_show_category_get(self):
        self.test_category.published = True
        self.test_category.save()
        url = reverse('tools:show_category', args=(self.test_category.id, ))
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/show_category.html')
        self.assertContains(resp, self.test_category.title)

    def test_show_category_get_unpublished(self):
        url = reverse('tools:show_category', args=(self.test_category.id, ))
        resp = self.client.get(url)
        self.assertEqual(404, resp.status_code)

    def test_add_category_get(self):
        self.client.login(username='testadmin', password='testpass')
        resp = self.client.get(reverse('tools:add_category'))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_category.html')
        self.assertContains(resp, 'Add Toolbox Section')

    def test_add_category_post(self):
        self.client.login(username='testadmin', password='testpass')
        empty = {}
        resp = self.client.post(
            reverse('tools:add_category'), empty, follow=True)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/add_category.html')
        self.assertContains(resp, 'Add Toolbox Section')
        test_group = CategoryGroup.objects.get(name='Other')
        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        data = {
            'title': 'our test title',
            'description': 'description test',
            'cover_image': test_fh,
            'resources_text': 'this changed',
            'group': test_group.id,
        }
        resp = self.client.post(reverse('tools:add_category'), data,
                                follow=True)

        actual = ToolCategory.objects.filter(title=data['title'])
        self.assertEqual(actual.count(), 1)
        category = actual[0]

        self.assertEqual(category.title, data['title'])
        self.assertEqual(category.description, data['description'])
        self.assertTrue(category.cover_image)
        self.assertTrue(category.cover_image.name, 'test empty.png')

        expected_url = 'http://testserver/tools/toolboxes/section/show/{}/'.format(
            category.id)
        self.assertEqual(
            [(expected_url, 302)], resp.redirect_chain)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You created a toolbox section", str(list(resp.context['messages'])[0]))

    def test_edit_category_get(self):
        self.client.login(username='testadmin', password='testpass')
        resp = self.client.get(reverse('tools:edit_category',
                                       args=(self.test_category.id,)))
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/edit_category.html')
        self.assertContains(resp, 'Edit Toolbox Section')
        self.assertContains(resp, self.test_category.title)
        self.assertContains(resp, self.test_category.description)

    def test_edit_category_post(self):
        self.client.login(username='testadmin', password='testpass')
        test_fh = SimpleUploadedFile('test empty.png', TEST_PNG_CONTENT)
        test_group = CategoryGroup.objects.get(name="Other")
        data = {
            'title': 'our category new title',
            'description': 'new category description test',
            'cover_image': test_fh,
            'resources_text': 'this changed',
            'group': test_group.id,
        }
        url = reverse('tools:edit_category', args=(self.test_category.id,))
        resp = self.client.post(url, data, follow=True)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(len(list(resp.context['messages'])), 1)
        self.assertEqual(
            "You updated this toolbox section",
            str(list(resp.context['messages'])[0])
        )
        self.assertContains(resp, data['title'])
        category = ToolCategory.objects.get(id=self.test_category.id)
        self.assertTrue(category.cover_image)
        self.assertTrue(category.cover_image.name, 'test empty.png')
        self.assertEqual(
            [('http://testserver/tools/toolboxes/section/show/%d/' % category.id,
              302)],
            resp.redirect_chain)

    def test_delete_category_get(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'tools:delete_category',
            args=(self.test_category.id, )
        )
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, 'tools/delete_category.html')
        self.assertContains(resp, 'Are you sure')

    def test_delete_category_post(self):
        self.client.login(username='testadmin', password='testpass')
        url = reverse(
            'tools:delete_category',
            args=(self.test_category.id, )
        )
        data = {'confirmation': 'yes'}
        resp = self.client.post(url, data, follow=True)
        expected_status = (
            'http://testserver/tools/toolboxes/',
            302
        )
        self.assertEqual([expected_status], resp.redirect_chain)
        self.assertFalse(ToolCategory.objects.exists())
        self.assertTrue(Tool.objects.filter(id=self.test_tool.id)
                        .exists())
        expected_tool_categories = Tool.objects.get(id=self.test_tool.id)\
            .categories.all().count()
        self.assertEqual(0, expected_tool_categories)
        self.assertTrue('messages' in resp.context)
        self.assertEqual(
            "You deleted a toolbox section",
            str(list(resp.context['messages'])[0])
        )
