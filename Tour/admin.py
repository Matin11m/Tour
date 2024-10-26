from django.contrib import admin
from .models import Category, Tour, TourImage, TourReport, BuyForm, Reservation


class TourReportInline(admin.TabularInline):
    model = TourReport
    extra = 1
    fields = ['day', 'report', 'image']


class BuyFormInline(admin.TabularInline):
    model = BuyForm
    extra = 1
    fields = ['first_name', 'last_name', 'national_id', 'birth_date', 'gender']


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


class ReservationAdmin:
    model = Reservation


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ['tour', 'image']


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', ]
    inlines = [TourImageInline, TourReportInline, BuyFormInline, ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(BuyForm)
class BuyFormAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'national_id', 'birth_date', 'gender']
    search_fields = ['first_name', 'last_name', 'national_id']
    list_filter = ['gender']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'reservation_date', 'status')
    list_filter = ('status', 'reservation_date')
    search_fields = ('user__username', 'tour__name')
    ordering = ('-reservation_date',)
    list_editable = ('status',)
