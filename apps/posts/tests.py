from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from users.tests import TestUtils

from forms import PostForm

# Test post form object directly
class PostFormTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
    def test_no_title(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'content' : 'This is content',} , author = author)
        self.assertFalse(form.is_valid())
    def test_no_content(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is title', } , author = author)
        self.assertFalse(form.is_valid())
    def test_author_title_content(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         } , author = author)
        self.assertTrue(form.is_valid())
    def test_duplicated_content_regardless_author(self): 
        author = User.objects.get(username = 'kecebongsoft')
        form1 = PostForm({'title' : 'This is title', 'content' : 'This is content',
                          } , author = author)
        
        form2 = PostForm({'title' : 'This is title', 'content' : 'This is content',
                          } , author = author)

        self.assertTrue(form1.is_valid())
        form1.save()

        self.assertFalse(form2.is_valid())
    def test_edit_post(self):
        author = User.objects.get(username = 'kecebongsoft')

        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         } , author = author)
        self.assertTrue(form.is_valid())
        post = form.save()
        
        form = PostForm({'title' : 'This is another title', 'content' : 'This is another content'},
                         instance = post, author = author)
        self.assertTrue(form.is_valid())

    
    def test_edit_post_different_user_admin(self):
        author = User.objects.get(username = 'kecebongsoft')

        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         } , author = author)
        self.assertTrue(form.is_valid())
        post = form.save()
        
        author_admin = User.objects.get(username = 'admin')
        form = PostForm({'title' : 'This is another title', 'content' : 'This is another content'},
                         instance = post, author = author_admin)
        self.assertTrue(form.is_valid())
    def test_edit_post_different_user_normal(self):
        author = User.objects.get(username = 'kecebongsoft')

        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         } , author = author)
        self.assertTrue(form.is_valid())
        post = form.save()
        
        author_normal = User.objects.get(username = 'dedi')
        form = PostForm({'title' : 'This is another title', 'content' : 'This is another content'},
                         instance = post, author = author_normal)
        self.assertFalse(form.is_valid())

    #Reply test
    def test_reply_no_title(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is a title', 'content' : 'This is a content'}, author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        author_reply = User.objects.get(username = 'dedi')
        form_reply = PostForm({'content' : 'This is a reply content'}, author = author_reply, parent = post)
        self.assertTrue(form_reply.is_valid())

    def test_reply_no_content(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is a title', 'content' : 'This is a content'}, author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        author_reply = User.objects.get(username = 'dedi')
        form_reply = PostForm({'content' : ''}, author = author_reply, parent = post)
        self.assertFalse(form_reply.is_valid())
    def test_reply_no_parent(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is a title', 'content' : 'This is a content'}, author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        author_reply = User.objects.get(username = 'dedi')
        form_reply = PostForm({'content' : 'This is a content'}, author = author_reply)
        self.assertFalse(form_reply.is_valid())
    def test_reply_valid(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is a title', 'content' : 'This is a content'}, author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        author_reply = User.objects.get(username = 'dedi')
        form_reply = PostForm({'content' : 'This is a reply content'}, author = author_reply, parent = post)
        self.assertTrue(form_reply.is_valid())

    def test_reply_duplicated_content_regardless_author(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is a title', 'content' : 'This is a content'}, author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        author_reply = User.objects.get(username = 'dedi')
        form_reply = PostForm({'content' : 'This is a reply content'}, author = author_reply, parent = post)
        self.assertTrue(form_reply.is_valid())
        form_reply.save()

        author_reply2 = User.objects.get(username = 'dedi')
        form_reply2 = PostForm({'content' : 'This is a reply content'}, author = author_reply2, parent = post)
        self.assertFalse(form_reply2.is_valid())

    def test_edit_reply_different_user_admin(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is a title', 'content' : 'This is a content'}, author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        author_reply = User.objects.get(username = 'dedi')
        form_reply = PostForm({'content' : 'This is a reply content'}, author = author_reply, parent = post)
        self.assertTrue(form_reply.is_valid())
        reply = form_reply.save()

        author_reply_admin = User.objects.get(username = 'admin')
        form_reply2 = PostForm({'content' : 'This is another reply content'}, instance = reply, author = author_reply_admin)
        self.assertTrue(form_reply2.is_valid())
        
    def test_edit_reply_different_user_normal(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is a title', 'content' : 'This is a content'}, author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        author_reply = User.objects.get(username = 'dedi')
        form_reply = PostForm({'content' : 'This is a reply content'}, author = author_reply, parent = post)
        self.assertTrue(form_reply.is_valid())
        reply = form_reply.save()

        author_reply_normal = User.objects.get(username = 'kecebongsoft')
        form_reply2 = PostForm({'content' : 'This is another reply content'}, instance = reply, author = author_reply_normal)
        self.assertFalse(form_reply2.is_valid())
        
# Test PostForm object via view
class PostTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
    def test_new_post(self):
        self.client.login(username = 'kecebongsoft', password='123')
        response = self.client.post(
            reverse('posts:new'),
            {
                'title' : 'This is title',
                'content' : 'This is content',
            }
        )
        # Should redirect to somewhere upon succesfully creating a new posts
        self.assertEqual(response.status_code, 302)

    def test_edit_post(self):
        author = User.objects.get(username = 'kecebongsoft')
        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         } , author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        self.client.login(username = 'kecebongsoft', password='123')
        response = self.client.post(
            reverse('posts:edit', args=[post.id]),
            {
                'title' : 'This is another title',
                'content' : 'This is another content',
            }
        )
        self.assertEqual(response.status_code, 302)
    def test_edit_post_different_user_admin(self):
        author = User.objects.get(username = 'kecebongsoft')

        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         } , author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        self.client.login(username = 'admin', password='123')
        response = self.client.post(
            reverse('posts:edit', args=[post.id]),
            {
                'title' : 'This is another title',
                'content' : 'This is another content',
            }
        )
        self.assertEqual(response.status_code, 302)
    def test_new_reply(self):
        author = User.objects.get(username = 'kecebongsoft')

        form = PostForm({'title' : 'This is title', 'content' : 'This is content',
                         } , author = author)
        self.assertTrue(form.is_valid())
        post = form.save()

        self.client.login(username = 'dedi', password='123')
        response = self.client.post(
            reverse('posts:new_reply', args=[post.id]),
            {
                'content' : 'This is a reply content',
            }
        )
        #Should redirect to somewhere upon succesful reply
        self.assertEqual(response.status_code, 302)
