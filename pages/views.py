from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic.edit import ModelFormMixin
from .models import Post,Comments
from .forms import CreateForm,LoginForm,UserUpdateForm, ProfileUpdateForm,CommentForm


def about(request):
	return render(request,'pages/about.html ')

def register(request):
	form=CreateForm()
	if request.method=="POST":
		form=CreateForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request,f'Account created for {username}')
			return redirect('page-login')
	context= {'form': form }
	return render(request,'pages/register.html',context)


def loginPage(request):
	form=LoginForm()
	if request.method=="POST":
		form=LoginForm(request.POST)
		if form.is_valid():
			user=authenticate(username=form.cleaned_data['username'] ,password=form.cleaned_data['password'])
			if user is not None:
				login(request,user)
				return redirect('page-profile')
			else:
				messages.error(request,f'Invalid username or password')
				return redirect('page-login')
			
	context={'form':form }
	return render(request,'pages/login.html',context)

def logoutUser(request):
	logout(request)
	return redirect('page-login')

@login_required
def account_settings(request):
	if request.method=="POST":
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request,'Your profile has been updated successfully')
			return redirect('page-profile')
	else:
		user_form = UserUpdateForm(instance=request.user)
		profile_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
	return render(request,'pages/account.html',context)


def profilePage(request):
	return render(request,'pages/profile.html')



class listPost(ListView):
	model=Post
	template_name='pages/home.html'
	context_object_name='posts'
	ordering=["-date_posted"]
	paginate_by = 5



def detailPost(request,pk):
    template_name = "pages/post_detail.html"
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )

class createPost(LoginRequiredMixin, CreateView):
	model=Post
	fields = ['title','content']
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(createPost,self).form_valid(form)


class userPostList(ListView):
	model = Post
	template_name = 'pages/user_posts.html'  
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')



class updatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model=Post
	fields = ['title','content']
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class deletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model=Post
	success_url = '/'
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
	
# Create your views here.
