from django.db import models
from datetime import date
from django_trucking import settings
from django.urls import reverse
from accounts.models import Customer, User, Driver


class Category(models.Model):
    """Типы кузова"""
    name = models.CharField("Тип кузова", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    

    class Meta:
        verbose_name = "Тип кузова"
        verbose_name_plural = "Типы кузова"


class Worker(models.Model):
    """Директоры и диспетчеры"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="workers/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('worker_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Директоры и диспетчеры"
        verbose_name_plural = "Директоры и диспетчеры"


class Type(models.Model):
    """Типы загрузки"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Типы загрузки"
        verbose_name_plural = "Типы загрузки"

class Pays(models.Model):
    """Типы оплаты"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип оплаты"
        verbose_name_plural = "Типы оплаты"



class Freight(models.Model):
    """Грузоперевозка"""
    title = models.CharField("Название", max_length=100)
    city1 = models.CharField("Загрузка", max_length=100, default='')
    description = models.TextField("Описание")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    city2 = models.CharField("Выгрузка", max_length=100, default='')
    directors = models.ManyToManyField(Worker, verbose_name="диспетчер", related_name="freight_director")
    workers = models.ManyToManyField(Worker, verbose_name="директор", related_name="freight_worker")
    types = models.ManyToManyField(Type, verbose_name="типы")
    pays = models.ManyToManyField(Pays, verbose_name="типы оплаты")
    date_to = models.DateField("Дата загрузки", default=date.today)
    date_off = models.DateField("Дата выгрузки", default=date.today)
    volume = models.PositiveIntegerField(
        "Объем груза", default=10, help_text="указывать в м3" 
    )
    weight = models.PositiveIntegerField(
        "Масса груза", default=0, help_text="указывать в тоннах"
    )
    sum = models.PositiveIntegerField(
        "Ставка", default=0, help_text="указывать сумму в рублях"
    )
    category = models.ForeignKey(
        Category, verbose_name="Тип кузова", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("freight_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Грузоперевозка"
        verbose_name_plural = "Грузоперевозки"


class Details(models.Model):
    """Детали"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    freight = models.ForeignKey(Freight, verbose_name="Грузоперевозка", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Детали"
        verbose_name_plural = "Детали"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    freight = models.ForeignKey(Freight, on_delete=models.CASCADE, verbose_name="грузоперевозка", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.freight}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    freight = models.ForeignKey(Freight, verbose_name="грузоперевозка", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.freight}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Status(models.Model):
    """Статус"""
    name1 = models.CharField("Имя", max_length=100)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name1

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Deal(models.Model):
    """Сделка"""
    title1 = models.CharField("Название", max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,)
    freight = models.ManyToManyField(Freight, verbose_name="грузоперевозка")
    documents = models.FileField("Договор", upload_to="documents/")
    status = models.ManyToManyField(Status, verbose_name="статус")
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.title1

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"

class Car(models.Model):
    """Авто"""
    title2 = models.CharField("Марка", max_length=100)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,)
    description = models.TextField("Описание")
    category = models.ForeignKey(
        Category, verbose_name="Тип кузова", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)

    def __str__(self):
        return self.title2


    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"


class News(models.Model):
    """Новости"""
    title3 = models.CharField("Заголовок", max_length=100)
    text = models.TextField("Текст")
    image = models.ImageField("Изображение", upload_to="news/")
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title3
    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.url})
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

