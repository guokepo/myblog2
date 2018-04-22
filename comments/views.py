from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.
def post_comment(request,post_pk):
    #先获取要评论的文章，get_object_or_404这个函数Post存在是则获取；否则返回404
    post = get_object_or_404(Post,pk=post_pk)

    #提交表单通过POST请求
    if request.method == 'POST':
        #上传数据到request,POST(类字典对象)
        #构造CommentForm实例，表单生成
        form = CommentForm(request.POST)

        #检查表单格式是否符合要求
        if form.is_valid():
            #合法则调用save()保存到数据库
            #commit=False仅仅生成Comment模型类实例，不将评论数据保存到数据库中
            comment = form.save(commit=False)
            #将评论与文章关联起来
            comment.post = post
            #将评论数据保存到数据库
            comment.save()
            #重定向到文章详情页
            return redirect(post)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
           # comment_set是一个特殊的模型管理器
            comment_list = post.comment_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list
            }

            return render(request,'blog/detail.html',context=context)
    #非POST请求返回到文章详情页
    return redirect(post)




