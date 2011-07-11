from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from users.tests import TestUtils

from posts.forms import PostForm
from .forms import TagForm

# When the user write a new posts, basically they need to provide 1 sticky tag (or we call it sub forum)
# and (optionally) a non-sticky tag (each non-sticky tag separated by comma)
# So in our tag form (which later will be combined with a Post form, we will have 2 fields
# The first field is for sticky tag, second one is an optional non-sticky tags
# User need to specify a sticky tag, and it MUST be a valid sticky tag (should be validated upon submitting)

# In this test case, we SHOULD include a Post form to simulate the real world case
class TagFormTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
    def test_new_post_no_sticky_tag(self): #should fail
        
    def test_new_post_no_non_sticky_tag(self): #should success
    def test_new_post_multiple_non_sticky_tag(self): #should success
    def test_edit_post(self): #should success

    # Adding tags in 
    def test_edit_tag(self):
class TagTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
    def test_new_post(self):
    def test_edit_post(self):
