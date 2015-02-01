from django.test import TestCase
from ..models import Entry, Tag
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime




class EntryModelTest(TestCase):

    def setUp(self):
        """
        set up defaut user
        """
        self.user = User.objects.create_user(
            'john', 'mail@mail.com', 'password')

    def create_entry(self, title, description):
        return Entry.objects.create(
            title=title, description=description, submitter=self.user)

    def test_construct_attr(self):
        e1 = self.create_entry("new1", description="normal day")
        self.assertEqual(e1.description, 'normal day')
        self.assertEqual(e1.title, 'new1')
        self.assertEqual(e1.submitter, self.user)

    def test_string_representation(self):
        e1 = self.create_entry("new1", description="normal day")
        self.assertEqual(str(e1), 'new1')

    def test_save_empty_description(self):
        e1 = self.create_entry("new1", description="")
        self.assertEqual(e1.description, '')

    def test_cant_save_empty_title(self):
        with self.assertRaises(ValidationError):
            e1 = self.create_entry("", "")
            e1.full_clean()

    def test_save_time_is_auto_add(self):
        e1 = self.create_entry("new1", description="normal day")
        self.assertIsInstance(e1.submitted_on, datetime)

    def test_entry_order(self):
        e1 = self.create_entry("new1", description="normal day")
        e2 = self.create_entry("new2", description="normal day")
        e3 = self.create_entry("new3", description="normal day")
        self.assertEqual(list(Entry.objects.all()), [e1, e2, e3])


class TagModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'john', 'mail@mail.com', 'password')
        self.e1 = Entry.objects.create(title="baseball", submitter=self.user)
        self.e2 = Entry.objects.create(title="Asia", submitter=self.user)
        self.e3 = Entry.objects.create(title="football", submitter=self.user)
        self.e4 = Entry.objects.create(title="EU", submitter=self.user)

    def create_tag(self, title, entrylist):
        t1 = Tag.objects.create(title=title)
        for e in entrylist:
            t1.entry.add(e)
        return t1

    def test_construct(self):
        t1 = self.create_tag('Sport', [self.e1, self.e3])
        t2 = self.create_tag('World', [self.e2, self.e4])

    def test_cant_save_empty_title(self):
        with self.assertRaises(ValidationError):
            t1 = self.create_tag("", [])
            t1.save()
            t1.full_clean()

    def test_string_representation(self):
        t1 = self.create_tag('Sport', [self.e1, self.e3])
        self.assertEqual(str(t1), 'Sport')

    def test_relate_to_entry(self):
        t1 = self.create_tag('Sport', [self.e1, self.e3])
        self.assertEqual(list(t1.entry.all()), [self.e1, self.e3])
        self.assertEqual(t1, self.e1.tag_set.all().first())

    def test_relate_to_entry_number(self):
        t1 = self.create_tag('Sport', [self.e1, self.e3])
        self.assertEqual(t1.entry.count(), 2)
