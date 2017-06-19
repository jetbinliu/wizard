from django.shortcuts import render

# Create your views here.
def mysql_backup(request):
    context = {}
    return render(request, 'bakconfig/mysql_backup.html', context)