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
        TestUtils.generate_tags()
        UserTestUtils.generate_users()
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                        } , author = author)
        self.post_form = form
        self.assertTrue(self.post_form.is_valid())
        self.post = self.post_form.save()
    def test_adding_existing_tag(self): #should fail
        tag = Tag()
        tag.name = "sticky1"
        tag.sticky = False #regardless the sticky flag (wtf is sticky flag?!)
        self.assertFalse(tag.save())
        
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
        self.assertEqual(self.post.tags.count(), 3)
    def test_single_non_sticky_tag(self): #should success
        form = TagForm({'tag_sticky' : 'sticky1', 
                        'tag_optional' : 'halo'},
                        post = self.post)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(self.post.tags.count(), 2)
    def test_multiple_non_sticky_tag(self): #should success
        form = TagForm({'tag_sticky' : 'sticky1', 
                        'tag_optional' : 'halo, satu,,,,, dua, tiga, empat,lima,enam,tujuh,lapan'},
                        post = self.post)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(self.post.tags.count(), 10)
    def test_clash_sticky_non_sticky_tag(self): #should fail
        form = TagForm({'tag_sticky' : 'sticky1', 
                        'tag_optional' : 'sticky2,testajah'},
                        post = self.post)
        self.assertFalse(form.is_valid())
    def test_edit_post(self): #should success (able to delete tags for that post and recreates it)
        
        #Assume we create a new post
        form = TagForm({'tag_sticky' : 'sticky1', 

                        'tag_optional' : 'anuku,testajah'})
        self.assertTrue(form.is_valid())
        form.post = self.post
        self.assertTrue(form.save())
        self.assertEqual(self.post.tags.count(), 3)
        
        #and we edit that post
        self.post.title = "this is another title"
        self.post.content = "this is another content"
        
        #can it delete all tags on this post and recreates it?
        form = TagForm({'tag_sticky' : 'sticky1', 
                        'tag_optional' : 'anukulagi, testajah, test lagih'},
                        post = self.post)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(self.post.tags.count(), 4)

class TagTest(TestCase):
    def setUp(self):
        UserTestUtils.generate_users()
        TestUtils.generate_tags()
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                        } , author = author)
        self.post_form = form
        self.assertTrue(self.post_form.is_valid())
        self.post = self.post_form.save()

    def test_new_post(self):
        self.client.login(username = 'kecebongsoft', password = '123')
        response = self.client.post(
            reverse('posts:new'),
            {
                'title' : 'This is new title',
                'content' : 'This is new content',
                'tag_sticky' : 'sticky1',
                'tag_optional' : 'a,b,c',
            }
        )
        # Should redirect to somewhere upon sucessfully creating a new posts
        self.assertEqual(response.status_code, 302)
    def test_edit_post(self):
        self.client.login(username = 'kecebongsoft', password = '123')
        
        response = self.client.post(
            reverse('posts:edit', args=[self.post.id]),
            {
                'title' : 'This is another title',
                'content' : 'This is another content',
                'tag_sticky' : 'sticky3',
                'tag_optional' : 'b,e,f',
            }
        )

        #Should redirect to somewhere upon sucessfully creating a new posts
        self.assertEqual(response.status_code, 302)
