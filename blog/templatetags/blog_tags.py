from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count


register = template.Library()
#实例化一个template.Library类，将get_recent_posts装饰为register.simple_tag


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_categories():
    #计算分类下的文章数，Count接受的是计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

tag_list = Tag.objects.annotate(num_posts=Count('post'))