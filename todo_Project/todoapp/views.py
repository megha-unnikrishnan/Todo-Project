from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .models import Task
from .forms import TodoTaskForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView



class Todolistview(ListView):
    model=Task
    template_name = 'home.html'
    context_object_name = 'task1'

class TodoDetailview(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class Todoupdateview(UpdateView):
    model=Task
    template_name = 'edit.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('detailview',kwargs={'pk':self.object.id})

class TodoDeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('listview')

class TodoCreateview(CreateView):
    model = Task
    fields = ('name','priority','date')
    template_name = 'data.html'
    success_url = reverse_lazy('listview')

def add(request):
    task1 = Task.objects.all()
    if request.method == 'POST':
        name=request.POST.get('name','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')
        task=Task(name=name,priority=priority,date=date)
        task.save()
    return render(request,'home.html',{'task1':task1})

def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    # if request.method == 'POST':
    #     if task.delete():
    #     return redirect('/')
    if 'yes' in request.POST:
        task.delete()
        return redirect('/')
    elif 'no' in request.POST:
        return redirect('/')
    else:
        pass
    return render(request,'delete.html',{'task':task})

def update(request,updateid):
    task=Task.objects.get(id=updateid)
    form=TodoTaskForm(request.POST or None,instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'update.html',{'task':task,'form':form})


# Create your views here.
