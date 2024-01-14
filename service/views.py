from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
from django.http import JsonResponse
from .models import GeneratedBlog, UserQuery
import google.generativeai as palm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Create your views here.

def index(request):
    return render(request, 'base.html')

# def generateBlog(request):
#     if request.method == "POST":
#         blog_title = request.POST.get('blog_title')
#         prompt = f'Write a blog on title {blog_title}'

#         try:
#             api_key = os.environ['GOOGLE_API_KEY']
#             # palm.configure(api_key=api_key)
#             # response = palm.chat(messages=[prompt])

#             # Assuming you have generated the blog content, replace 'generated_content' with the actual content
#             blog_content_generate = "response.last"
#             print(blog_content_generate)
            
#             if blog_content_generate:
#                 blog_title = blog_title
#                 blog_content = blog_content_generate
#                 print(blog_title)
#                 print(blog_content)
#                 # Save the blog content to the database
#                 blog = GeneratedBlog.objects.create(blog_title=blog_title, blog_content=blog_content)
#                 blog.save()
#             else:
#                 return HttpResponseServerError('Internal Server Error: Error generating blog content')
                
#             url = 'getBlog/?blog_title={}'.format(blog_title)
#             # Redirect to saveBlog with the necessary parameters
#             return redirect(url)

#         except KeyError:
#             # Handle the case where the GOOGLE_API_KEY is missing from the environment variables
#             return HttpResponseServerError('Internal Server Error: API key is missing')

#         except Exception as e:
#             # Handle other exceptions, log the error, and return an appropriate response
#             print(f'Error: {e}')
#             return HttpResponseServerError('Internal Server Error1')

#     return HttpResponseServerError('Invalid request method')

# # def saveBlog(request):
# #     if request.method == "GET":
# #         try:
# #             blog_title = request.GET.get('blog_title')
# #             blog_content = request.GET.get('blog_content')
# #             print(blog_title)
# #             print(blog_content)
# #             # Save the blog content to the database
# #             blog = GeneratedBlog.objects.create(blog_title=blog_title, blog_content=blog_content)
# #             blog.save()

# #             url = 'getBlog'
# #             return redirect(url, blog_title=blog_title)

# #         except Exception as e:
# #             # Handle exceptions related to saving the blog
# #             print(f'Error saving blog: {e}')
# #             return HttpResponseServerError('Internal Server Error: Error saving blog')

# def getBlog(request):
#     if request.method == "GET":
#         try:
#             blog_title = request.GET.get('blog_title')
#             blog = GeneratedBlog.objects.get(blog_title=blog_title)
#             context = {'blog': blog}
#             # print(f'Get Blog: {blog.blog_content}')
#         except GeneratedBlog.DoesNotExist:
#             context = {'error_message': 'Blog not found'}

#     return render(request, 'base.html', context)

def generateBlog(request):
    if request.method == "POST":
        # Your existing code...
        blog_title = request.POST.get('blog_title')
        selected_value = request.POST.get('type_select')
        prompt = f'Write a blog on title {blog_title} and type should be {selected_value}'
        blog_content_generate = 'response.last'

        if blog_content_generate:
            blog_title = blog_title
            blog_content = blog_content_generate

            # Save the blog content to the database
            blog = GeneratedBlog.objects.create(blog_title=blog_title, blog_type=selected_value ,blog_content=blog_content)
            blog.save()

            # Construct the URL without the need for a redirect
            url = f'/getBlog/?blog_title={blog_title}'

            # Return the new URL as a JSON response
            return JsonResponse({'url': url, 'generated_content': blog_content})
        else:
            return HttpResponseServerError('Internal Server Error: Error generating blog content')

    return HttpResponseServerError('Invalid request method')

def getBlog(request):
    if request.method == "GET":
        try:
            blog_title = request.GET.get('blog_title')
            blog = GeneratedBlog.objects.get(blog_title=blog_title)
            context = {'blog': blog}
            return render(request, 'base.html', context)
        except GeneratedBlog.DoesNotExist:
            context = {'error_message': 'Blog not found'}
            return render(request, 'base.html', context)

def user_query(request):
    if request.method == "POST":
        user_email = request.POST.get('user_email')
        user_query = request.POST.get('user_query')
        # Save the blog content to the database
        user = UserQuery.objects.create(user_email=user_email, user_query=user_query)
        user.save()

        context = {'success': 'Your response has been reached to us!'}
    else:
        context = {'error': 'Sorry we can not get your response!'}

    return redirect('/', context)


def update_like_dislike(request, blog_title):
    if request.method == 'POST':
        try:
            # Parse JSON from the request body
            data = json.loads(request.body.decode('utf-8'))

            # Get the 'is_like' value from the payload
            is_like = data.get('is_like')  # Default to False if 'is_like' is not present

            # Rest of your view logic...
            blog = get_object_or_404(GeneratedBlog, blog_title=blog_title)

            # Update the model based on the 'is_like' value
            blog.reward = is_like
            blog.save()

            return JsonResponse({'message': 'Updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON in request body'}, status=400)
    
    return JsonResponse({'message': 'Invalid request method'}, status=400)