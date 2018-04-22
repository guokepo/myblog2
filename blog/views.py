from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post,Category
import markdown
from comments.forms import CommentForm


# Create your views here.
#from django.http import HttpResponse

def index(request):
    post_list = Post.objects.all() #.order_by('-created_time')#已在models中进行了排序
    return render(request, 'blog/index.html', context={'post_list': post_list})



def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #引入Markdown标记语言进行文本编辑
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    #获取本篇文章下的全部评论
    comment_list = post.comment_set.all()
    #将下列三个作为变量传给detail.html渲染
    context = {'post':post,
               'form':form,
               'comment_list':comment_list
    }


    return render(request, 'blog/detail.html', context=context)


def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})