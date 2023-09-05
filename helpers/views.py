from django.shortcuts import render


def handle_not_found(request, exception):
    """
    HTTP 404 Not Found hatasını yakalar ve Html Render ile önceden hazırlanmış sayfayı döner.
    """
    return render(request, 'helpers/not-found.html')


def handle_server_error(request):
    """
    HTTP 500 Server Error hatasını yakalar ve Html Render ile önceden hazırlanmış sayfayı döner.
    """
    return render(request, 'helpers/server-error.html')