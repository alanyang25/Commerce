from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORY = (
        ("Fashion", "fashion"),
        ("Toys", "toys"),
        ("Electronics", "electronics"),
        ("Home", "home"),
        ("Sports", "sports")
    )
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY, default="Fashion")
    description = models.CharField(max_length=600)
    current_price = models.FloatField(null=True, default=None)
    image_link = models.CharField(max_length=128, default=None, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='created_by')
    created_on = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    published  = models.BooleanField(null=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name='watchlist')
    winner = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name='winner')
    
    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", default=None, null=True)
    auction_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="auction_bid", default=None, null=True)
    bid_time = models.DateTimeField(blank=True, null=True)
    bid_price = models.FloatField(null=True, default=None)

    def __str__(self):
        return f"{self.bidder} bid on {self.auction_id} with ${self.bid_price}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter', default=None, null=True)
    auction_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='auction_comment', default=None, null=True)
    comment_title = models.CharField(max_length=50)
    comment_content = models.CharField(max_length=600)
    comment_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.commenter} comment on {self.auction_id}"

