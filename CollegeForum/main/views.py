from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.
def homePage(request):
	return render(request, 'mainpage.html')

def allQuestionPage(request, tag):
	questions = Question.objects.filter(tag=tag).order_by('-created_at')
	return render(request, 'home-page.html', {
		'questions': questions,
		'tag': tag
	})

def allBlogPage(request, tag):
	blogs = Blog.objects.filter(tag=tag).order_by('-created_at')
	return render(request, 'blog-page.html', {
		'blogs': blogs,
		'tag': tag,
	})

def registerPage(request):
	if request.method == 'POST':
		try:
			form = RegisterUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				login(request, user)
				return redirect('index')
		except Exception as e:
			print(e)
			raise
	return render(request, 'register.html', {
		'form': RegisterUserForm()
	})

def loginPage(request):
	if request.method == 'POST':
		try:
			form = LoginForm(data=request.POST)
			if form.is_valid():
				user = form.get_user()
				login(request, user)
				return redirect('index')
		except Exception as e:
			print(e)
			raise
	return render(request, 'login.html', {
		'form': LoginForm()
	})

@login_required(login_url='register')
def logoutPage(request):
	logout(request)
	return redirect('login')

def blogPage(request, tag, id):
	response_form = NewBlogResponseForm()	
	if request.method == 'POST':
		try:
			response_form = NewBlogResponseForm(request.POST)
			if response_form.is_valid():
				response = response_form.save(commit=False)
				response.user = request.user
				response.blog = Blog(id=id)
				response.save()
				return redirect('blog', tag=tag, id=id)
		except Exception as e:
			print(e)
			raise
		
	blog = Blog.objects.get(id=id)
	return render(request, 'blog.html', {
		'blog': blog,
        'blog_response_form': response_form,
		'tag': tag,
	})

def questionPage(request, tag, id):
	response_form = NewResponseForm()
	reply_form = NewReplyForm()
	
	if request.method == 'POST':
		try:
			response_form = NewResponseForm(request.POST)
			if response_form.is_valid():
				response = response_form.save(commit=False)
				response.user = request.user
				response.question = Question(id=id)
				response.save()
				return redirect('question', tag= tag, id= id)
		except Exception as e:
			print(e)
			raise
		
	question = Question.objects.get(id=id)
	return render(request, 'question.html', {
		'question': question,
        'response_form': response_form,
		'reply_form': reply_form,
		'tag': tag,
	})

@login_required(login_url='register')
def newBlog(request, tag):
	if request.method == 'POST':
		try:
			form = NewBlogForm(request.POST)
			if form.is_valid():
				blog = form.save(commit=False)
				blog.author = request.user
				blog.tag = tag
				blog.save()
				return redirect('all-blog', tag=tag)
		except Exception as e:
			print(e)
			raise
	return render(request, 'new-blog.html', {
		'form': NewBlogForm()
	})

@login_required(login_url='register')
def newQquestion(request, tag):
	if request.method == 'POST':
		try:
			form = NewQuestionForm(request.POST)
			if form.is_valid():
				question = form.save(commit=False)
				question.author = request.user
				question.tag = tag
				question.save()
				return redirect('all-questions', tag=tag)
		except Exception as e:
			print(e)
			raise
	return render(request, 'new-question.html', {
		'form': NewQuestionForm()
	})

@login_required(login_url='register')
def replyPage(request):
	if request.method == 'POST':
		try:
			form = NewReplyForm(request.POST)
			if form.is_valid():
				question_id = request.POST.get('question')
				parent_id = request.POST.get('parent')
				tag = request.POST.get('tag')
				reply = form.save(commit=False)
				reply.user = request.user
				reply.question = Question(id=question_id)
				reply.parent = Response(id=parent_id)
				reply.save()
				return redirect('question', id=question_id, tag=tag)
		except Exception as e:
			print(e)
			raise

	return redirect('index')