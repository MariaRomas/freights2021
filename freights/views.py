from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View
from .models import Freight, Category, Worker, Type, Rating, Pays, Car, News
from .forms import ReviewForm, RatingForm
from django.db.models import Q
from django.http import JsonResponse, HttpResponse


class TypePay:
    """Типы загрузки и оплаты"""
    def get_types(self):
        return Type.objects.all()
        
    def get_pays(self):
        return Pays.objects.all()

    def get_categories(self):
        return Category.objects.all()



def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
   

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'freights/index.html',
   
    )

def about(request):
   
    return render(
        request,
        'freights/about.html',
   
    )

def contacts(request):
   
    return render(
        request,
        'freights/contacts.html',
   
    )

class FreightsView(TypePay, ListView):
    """Список грузов"""
    model = Freight
    queryset = Freight.objects.filter(draft=False)
    paginate_by = 6
    template_name = 'freights/freight_list.html'

class CarsView(TypePay, ListView):
    """Список авто"""
    model = Car
    template_name = 'freights/car_list.html'
    queryset = Car.objects.all()

class NewsView(ListView):
    """Список новостей"""
    model = News
    template_name = 'freights/news_list.html'
    queryset = News.objects.all()

class NewsDetailView(DetailView):
    """Полное описание """
    model = News
    slug_field = "url"

    

class AddStarRating(View):
    """Добавление рейтинга грузоперевозки"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip  
    

class FreightDetailView(TypePay, DetailView):
    """Полное описание грузоперевозки"""
    model = Freight
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context

  
    
class AddReview(View):
    """Запросы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        freight = Freight.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.freight = freight
            form.save()
            return redirect(freight.get_absolute_url())



class WorkerView(TypePay, DetailView):
    """Вывод информации о работнике"""
    model = Worker
    template_name = 'freights/worker.html'
    slug_field = "name"

class FilterFreightsView(TypePay, ListView):
    """Фильтр грузоперевозок"""
    paginate_by = 6
    def get_queryset(self):
        queryset = Freight.objects.filter(
            Q(types__in=self.request.GET.getlist("type"))|
            Q(pays__in=self.request.GET.getlist("pay"))|
            Q(category__in=self.request.GET.getlist("pay"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["type"] = ''.join([f"type={x}&" for x in self.request.GET.getlist("type")])
        context["pay"] = ''.join([f"pay={x}&" for x in self.request.GET.getlist("pay")])
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        return context

class JsonFilterFreightsView(ListView):
    """Фильтр грузов в json"""
    def get_queryset(self):
        queryset = Freight.objects.filter(
            Q(pays__in=self.request.GET.getlist("pay")) |
            Q(types__in=self.request.GET.getlist("type"))
        ).distinct().values("title", "city1", "url")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"freight": queryset}, safe=False)

class AddStarRating(View):
    """Добавление рейтинга грузоперевозке"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                freight_id=int(request.POST.get("freight")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class Search(ListView):
    """Поиск грузов"""
    paginate_by = 6
    

    def get_queryset(self):
        return Freight.objects.filter(city1__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context