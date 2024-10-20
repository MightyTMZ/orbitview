from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

"""
Purpose: Manages articles, videos, infographics, and other media produced by your platform.
Features:
- CRUD (Create, Read, Update, Delete) operations for content
- Categories/tags for organizing content
- Integration with rich text editors for article creation
- Uploading and embedding media (images, videos, etc.)
- Commenting and content feedback
"""


"""
Model classes:

- Video {
    - id
    - unique_code (UUID)
    - title
    - video (file)
    - creator (user)

}
- Post (come up with an innovative post structure that is different
from Instagram, LinkedIn, YouTube, etc. )

- Article
- 

"""

"""
Innovative Post Structure:
1. Content Type: Multi-Layered Posts

Users can create multi-layered posts that go beyond simple text or images. Each post can have different content layers, like:
Main Post: A core message or update (text, image, or video).
Call-to-Action Layer: Interactive buttons such as "Ask for Feedback," "Connect," or "Participate."
Insight Layer: Post highlights AI-suggested trends, relevant data, or personalized stats based on the content, enriching the user experience.
Survey or Question Layer: Add polls, interactive quizzes, or real-time decision-based questions for engagement.
Example: A post about launching a product could include a video, a quick poll for users’ feedback on features, and a "Learn More" button directing users to in-depth resources.

2. Dynamic Threads:

Posts are presented as expandable threads, where users can click to see deeper insights. For example, a user can post a main point (e.g., "Excited about this AI project!") and allow followers to expand the post to see behind-the-scenes updates, in-depth breakdowns, or interactive modules that explain concepts.
Example: A short status about attending a conference could expand to show detailed schedules, speaker insights, and personalized event recommendations.

3. Post Customization:

Posts can be customized based on viewer preferences. For example:
Mini-Courses/Post Series: Users can create a "progressive post" series, allowing followers to unlock parts of the post over time (ideal for tutorials, stories, or challenges).
Topic Tags & Suggestions: Users receive personalized content based on their interest in the post’s topic (e.g., “You viewed this tech update, here are related courses or events.”)
4. Time Capsule Posts:

Users can create “Time Capsule” posts where they set posts to reappear in their feed after a set period of time. These posts could include future goals, challenges, or reflections, creating a unique engagement loop.
5. Collaborative Post:

Allow multiple users to contribute to a single post (like collaborative storytelling or project building), where others can co-create content. This would give posts a more community-driven and co-creative feel.
Why Consumers Would Love This:
Personalization: Posts automatically adjust based on interests, offering personalized content or suggestions.
Interactivity: Posts are not static—they invite engagement, learning, and interaction, making the experience richer.
Progressive Content Delivery: Unlockable post series create intrigue and sustained engagement over time.
Multi-Layered Content: Consumers can engage on different levels, from basic interactions to deep insights, based on their preferences.
This approach offers a dynamic and engaging way for users to interact with content beyond simple likes and comments, turning posts into personalized experiences.
"""

from django.db import models
import uuid


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/') # use a CDN afterwards
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MultiLayeredPost(models.Model):
    POST_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('POLL', 'Poll'),
        ('QUIZ', 'Quiz'),
        ('CTA', 'Call to Action'),
    ]
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)
    main_content = models.TextField(null=True, blank=True)  # Could be text, link, etc.
    # attachment = models.FileField(upload_to='post_attachments/', null=True, blank=True)  # image, video, etc.
    interactive_layer = models.JSONField(default=dict)  # polls, quizzes, CTA buttons, insights, etc.
    timestamp = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    # If a post is archived, it will not be shown, similar to how Instagram does it

    def __str__(self):
        return f'Post by {self.author.username}'

    def add_interaction(self, layer_type, content):
        """Adds a new layer of interaction to the post."""
        if layer_type not in ['poll', 'quiz', 'cta']:
            raise ValueError("Invalid interaction layer type")
        self.interactive_layer[layer_type] = content
        self.save()


class PostAttachment(models.Model):
    attachment = models.FileField(upload_to='post_attachments/')
    post = models.ForeignKey(MultiLayeredPost, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(MultiLayeredPost, on_delete=models.CASCADE, related_name='comments')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
    comment_contents = models.TextField(max_length=1500)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies') 

    # We use a self-referencing foreign key

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.creator} on {self.post}'

    @property
    def is_reply(self):
        return self.parent is not None



class TimeCapsulePost(models.Model):
    post = models.OneToOneField(MultiLayeredPost, on_delete=models.CASCADE, related_name='time_capsule')
    reveal_date = models.DateTimeField()

    def __str__(self):
        return f'Time Capsule Post - Reveal on {self.reveal_date}'


class CollaborativePost(models.Model):
    id = models.AutoField(primary_key=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collaborative_posts')
    main_post = models.OneToOneField(MultiLayeredPost, on_delete=models.CASCADE, related_name='collaborative_post')
    collaboration_message = models.TextField(max_length=5000) # cannot go more than 5000 characters

    def __str__(self):
        return f'Collaborative Post with {", ".join([user.username for user in self.contributors.all()])}'


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = RichTextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

