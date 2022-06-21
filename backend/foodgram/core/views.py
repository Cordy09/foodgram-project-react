from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, {'path': request.path}, status=404)


def integrity_error(request):
    return render(request, {'path': request.path}, status=400)
