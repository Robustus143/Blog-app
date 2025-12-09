import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.models import Post

def run():
    print("Starting reproduction script...")
    User = get_user_model()
    
    # Create or get users
    user1, _ = User.objects.get_or_create(username='testuser1')
    user1.set_password('pass')
    user1.save()
    
    user2, _ = User.objects.get_or_create(username='testuser2')
    user2.set_password('pass')
    user2.save()
    
    # Cleanup old posts
    Post.objects.filter(title='Test Post Repro').delete()

    # Create post
    post = Post.objects.create(author=user1, title='Test Post Repro', text='Test Content')
    post.publish()
    
    print(f"Post created: {post} (pk={post.pk})")
    
    # Add 1 like
    post.likes.add(user1)
    print(f"Likes count: {post.likes.count()}")
    
    factory = RequestFactory()
    request = factory.get('/')
    request.user = user1

    # Render with 1 like
    try:
        render_to_string('blog/post_list.html', {'posts': [post]}, request=request)
        print("Render with 1 like: SUCCESS")
    except Exception as e:
        print(f"Render with 1 like: FAILED - {e}")

    # Add 2nd like
    post.likes.add(user2)
    print(f"Likes count: {post.likes.count()}")
    
    # Render with 2 likes
    try:
        content = render_to_string('blog/post_list.html', {'posts': [post]}, request=request)
        print("Render with 2 likes: SUCCESS")
    except Exception as e:
        print(f"Render with 2 likes: FAILED - {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    from django.template.loader import render_to_string
    run()
