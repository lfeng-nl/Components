from django.shortcuts import render

# Create your views here.

def home(request):
    navigation = ['变量', '循环', '条件判断', '过滤器']
    info = {
        navigation[0]:r"{{ string }}",
        navigation[1]:r'{% for x in list %}  {% endfor %}',
        navigation[2]:r'{% if xxx %}',
        navigation[3]:r'{{ var|length }}'
    }
    return render(request, 'home.html', {'Navigation': navigation, 'info':info})

def more(request):
    return render(request, 'more.html')