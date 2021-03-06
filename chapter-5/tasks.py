from celery import Celery
import os
import urllib
from django.dispatch import receiver
from django.db.models.signals import post_save
from mezzanine.generic.models import ThreadedComment

AWS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET = os.getenv('AWS_SECRET_ACCESS_KEY')
if not (AWS_KEY and AWS_SECRET):
        print "AWS environment variables are not set\n"
        exit(1)

app = Celery('tasks', broker = 'sqs://@')

def is_comment_spam(comment):
    # This check is just an example!
    if "spam" in comment.comment:
        return True

@app.task
def process_comment_async(comment_id):
    print "Processing comment"
    comment = ThreadedComment.objects.get(pk=comment_id)
    if is_comment_spam(comment):
        # The comment is spam, so hide it
        ThreadedComment.objects.filter(id=comment_id).update(is_public=False)

@receiver(post_save, sender=ThreadedComment)
def process_comment(sender, instance, **kwargs):
    process_comment_async.delay(instance.id)
