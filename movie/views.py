from django.shortcuts import render

# Create your views here.
def MovieCreateView(request):
    return render(request, 'movie_create_form.html', {
        'data': "Hello Django ",
    })