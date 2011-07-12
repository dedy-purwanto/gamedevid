from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from users.tests import TestUtils as UserTestUtils

from posts.forms import PostForm
from .forms import TagForm
from .models import Tag, TagPost
# When the user write a new posts, basically they need to provide 1 sticky tag (or we call it sub forum)
# and (optionally) a non-sticky tag (each non-sticky tag separated by comma)
# So in our tag form (which later will be combined with a Post form, we will have 2 fields
# The first field is for sticky tag, second one is an optional non-sticky tags
# User need to specify a sticky tag, and it MUST be a valid sticky tag (should be validated upon submitting)

# In this test case, we SHOULD include a Post form to simulate the real world case
class TestUtils():
    @staticmethod
    def generate_tags():
        tags = (
                ('sticky1', True),
                ('sticky2', True),
                ('sticky3', True),
                ('sticky4', True),
                ('not_sticky1', False),
                ('not_sticky2', False),
               )
        for t in tags:
            tag = Tag()
            tag.name = t[0]
            tag.sticky = t[1]
            tag.save()
class TagFormTest(TestCase):
    def setUp(self):
        TagUtils.generate_tags()
        UserTestUtils.generate_users()

        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                        } , author = author)
        self.post_form = form
        self.assertTrue(self.post_form.is_valid())
        self.post = self.post_form.save()

        tag = Tag()
        tag.name = 'sticky_tag'
        tag.sticky = True
        tag.save()
    def test_no_sticky_tag(self): #should fail
        form = TagForm({'tag_sticky' : '', 
                        'tag_optional' : 'tag1, tag2'},
                        post = self.post)
        self.assertFalse(form.is_valid())
    def test_invalid_sticky_tag(self): #should fail
        form = TagForm({'tag_sticky' : 'sticky_not_exist', 
                        'tag_optional' : 'tag1, non_sticky1'},
                        post = self.post)
        self.assertFalse(form.is_valid())
    def test_multiple_sticky_tag(self): #should fail
        form = TagForm({'tag_sticky' : 'sticky1,sticky2', 
                        'tag_optional' : 'tag1, non_sticky2'},
                        post = self.post)
        self.assertFalse(form.is_valid())
    def test_no_non_sticky_tag(self): #should success
        form = TagForm({'tag_sticky' : 'sticky1', 
                        'tag_optional' : 'non_sticky1, test aja'},
                        post = self.post)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(TagPost.get_tags(self.post).count(), 2)
    def test_single_non_sticky_tag(self): #should success
        form = TagForm({'tag_sticky' : 'sticky1', 
                        'tag_optional' : 'halo'},
                        post = self.post)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(TagPost.get_tags(self.post).count(), 2)
    def test_multiple_non_sticky_tag(self): #should success
        form = TagForm({'tag_sticky' : 'sticky1', 
                        'tag_optional' : 'halo, satu,,,,, dua, tiga, empat,lima,enam,tujuh,lapan'},
                        post = self.post)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(TagPost.get_tags(self.post).count(), 9)
    def test_clash_sticky_non_sticky_tag(self): #should fail
        form = TagForm({'tag_sticky' : 'sticky1', 
                        'tag_optional' : 'sticky2,testajah'},
                        post = self.post)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(TagPost.get_tags(self.post).count(), 2)
    def test_edit_post(self): #should success (able to delete tags for that post and recreates it)
        
        #Assume we create a new post
        form = TagForm({'tag_sticky' : 'sticky1', 

                        'tag_optional' : 'sticky2,testajah'},
                        post = self.post)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(TagPost.get_tags(post).count(), 2)
        
        #and we edit that post
        self.post.title = "this is another title"
        self.post.content = "this is another content"
        
        #can it delete all tags on this post and recreates it?
        form = TagForm({'tag_sticky' : 'sticky1', 
                        'tag_optional' : 'sticky2, testajah, test lagih'},
                        post = self.post)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(TagPost,get_tags(post).count(), 3)

class TagTest(TestCase):
    def setUp(self):
        UserTestUtils.generate_users()
        TestUtils.generate_tags()
    def test_new_post(self):
        
    def test_edit_post(self):
