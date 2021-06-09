from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Type, User, Freight, Details, Worker, Rating, RatingStar, Reviews, Pays, Status, Deal, Car, News
from ckeditor_uploader.widgets import CKEditorUploadingWidget




class FreightAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
   
    class Meta:
        model = Freight
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Типы кузова"""
    list_display = ("name",   "url")
    list_display_links = ("name",)



class ReviewInline(admin.TabularInline):
    """Отзывы на странице грузоперевозки"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")

class DetailsInline(admin.TabularInline):
    model = Details
    extra = 1
   
    
@admin.register(Freight)
class FreightAdmin(admin.ModelAdmin):
    
    list_display = ("title", "category", "url", "draft", "author")
    list_filter = ("types", "category")
    search_fields = ("title", "category__name")
    inlines = [ DetailsInline, ReviewInline]
    form = FreightAdminForm
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    fieldsets = (
       
        (None, {
            "fields": (("title", "city1", "city2"),)
        }),
        (None, {
            "fields": ("description",)
        }),
        (None, {
            "fields": (("date_to", "date_off"),)
        }),
        ("Workers", {
            "classes": ("collapse",),
            "fields": (("workers", "directors", "types", "pays", "category"),)
        }),
        (None, {
            "fields": (("weight", "volume", "sum"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )
    
    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(FreightAdmin, self).get_queryset(request)
        else:
            qs = super(FreightAdmin, self).get_queryset(request)
            return qs.filter(author=request.user)
    
    def save_model(self, request, obj, form, change):
        freight = form.save(commit=False)
        freight.author = request.user
        freight.save()
        super(FreightAdmin, self).save_model(request, obj, form, change)
    

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )
    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "freight", "id")
    readonly_fields = ("name", "email")
    

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """Типы загрузки"""
    list_display = ("name", "url")

@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    """Типы оплаты"""
    list_display = ("name", "url")

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Статусы"""
    list_display = ("name1", "url")

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    """Директоры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')
        get_image.short_description = "Изображение" 

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "freight",  "ip")


@admin.register(Details)
class DetailsAdmin(admin.ModelAdmin):
    """Детали из грузоперевозок"""
    list_display = ("title", "freight")


admin.site.register(RatingStar)
admin.site.site_title = "Грузоперевозки"
admin.site.site_header = "Грузоперевозки"


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """Сделки"""
    list_display = ("title1", "url")
    fieldsets = (
       
        (None, {
            "fields": (("title1", "customer", "driver"),)
        }),
        (None, {
            "fields": ("freight",)
        }),
        (None, {
            "fields": (("documents", "status"),)
        }),
        ("Options", {
            "fields": (("url",),)
        }),
    )

    def show_name():
        customers = User.objects.filter(groups__name='customer')
        return customers
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Новости"""
    list_display = ("title3", "url", "draft")
   

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Авто"""
    list_display = ("title2",  "category", "url")
 
        
    