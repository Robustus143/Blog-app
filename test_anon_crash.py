import os
import django
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.template import Context, Template

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.models import Post
from django.contrib.auth import get_user_model

def run():
    User = get_user_model()
    # Create a user to like the post
    u1, _ = User.objects.get_or_create(username='u1')
    u2, _ = User.objects.get_or_create(username='u2')
    
    # Create a post
    post = Post.objects.create(author=u1, title='Test Crash', text='content')
    post.likes.add(u1)
    post.likes.add(u2)
    
    # Test 1: Check if AnonymousUser in likes.all() crashes
    anon = AnonymousUser()
    try:
        print(f"Checking AnonymousUser in post.likes.all()...")
        res = anon in post.likes.all()
        print(f"Result: {res}")
    except Exception as e:
        print(f"CRASHED with AnonymousUser: {e}")

    # Test 2: Check template rendering
    t = Template("{% if user in post.likes.all %}Liked{% else %}Not Liked{% endif %}")
    c = Context({'user': anon, 'post': post})
    try:
        print("Rendering template...")
        rendered = t.render(c)
        print(f"Rendered: {rendered}")
    except Exception as e:
        print(f"Template CRASHED: {e}")

    # Cleanup
    post.delete()

if __name__ == '__main__':
    run()
