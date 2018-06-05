from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post,Category
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
#from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
#from django.http import HttpResponse
#每一个视图函数都有它对应的类的对应视图
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

def index(request):
    post_list = Post.objects.all() #.order_by('-created_time')#已在models中进行了排序
    return render(request, 'blog/index.html', context={'post_list': post_list})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        #调用父类get方法后才能获得self.object属性即为访问的文章
        response = super(PostDetailView, self).get(request,*args,**kwargs)

        #文章（self.object）阅读量
        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        # 对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        #将post传递给模板，同时将评论表单，post下的评论列表传递给模板
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context



def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    #调用阅读量函数
    post.increase_views()

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

class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month)

def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})