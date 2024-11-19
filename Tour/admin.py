# from django.contrib import admin
# from .models import Category, Tour, TourImage, TourReport, BuyForm, Reservation
#
#
# class TourReportInline(admin.TabularInline):
#     model = TourReport
#     extra = 1
#     fields = ['day', 'report', 'image']
#
#
# class BuyFormInline(admin.TabularInline):
#     model = BuyForm
#     extra = 1
#     fields = ['first_name', 'last_name', 'national_id', 'birth_date', 'gender']
#
#
# class TourImageInline(admin.TabularInline):
#     model = TourImage
#     extra = 1
#
#
# class ReservationAdmin:
#     model = Reservation
#
#
# @admin.register(TourImage)
# class TourImageAdmin(admin.ModelAdmin):
#     list_display = ['tour', 'image']
#
#
# @admin.register(Tour)
# class TourAdmin(admin.ModelAdmin):
#     list_display = ['name', 'category', ]
#     inlines = [TourImageInline, TourReportInline, BuyFormInline, ]
#
#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name']
#
#
# @admin.register(BuyForm)
# class BuyFormAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'national_id', 'birth_date', 'gender']
#     search_fields = ['first_name', 'last_name', 'national_id']
#     list_filter = ['gender']
#
#
# @admin.register(Reservation)
# class ReservationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'tour', 'reservation_date', 'status')
#     list_filter = ('status', 'reservation_date')
#     search_fields = ('user__username', 'tour__name')
#     ordering = ('-reservation_date',)
#     list_editable = ('status',)


from django.contrib import admin
from .models import (
    UserProfile, City, Category, Tour,
    Trip, Favorite, Comment, Passenger, Order,
    Transaction, Refund, Banner, TourReport, TourImage
)


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


class TourReportInline(admin.TabularInline):
    model = TourReport
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'city', 'description', 'stay')
    search_fields = ('title', 'category__title', 'city__name')
    list_filter = ('category', 'city')
    inlines = [TourImageInline, TourReportInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'national_id')
    search_fields = ('user__username', 'first_name', 'last_name', 'national_id')


# @admin.register(Province)
# class ProvinceAdmin(admin.ModelAdmin):
#     list_display = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'parent')
    search_fields = ('title',)
    list_filter = ('parent',)


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ('tour', 'image')


@admin.register(TourReport)
class TourReportAdmin(admin.ModelAdmin):
    list_display = ('tour', 'day', 'report')


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('tour', 'price', 'discount_price', 'capacity', 'start_date', 'end_date')
    search_fields = ('tour__title',)
    list_filter = ('start_date', 'end_date')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour')
    search_fields = ('user__username', 'tour__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'score', 'visibility')
    search_fields = ('user__username', 'tour__title', 'text')
    list_filter = ('visibility',)


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'national_id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'trip', 'price', 'adults_number', 'children_number', 'order_status', 'payment_status')
    search_fields = ('user__username', 'trip__tour__title')
    list_filter = ('order_status', 'payment_status')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'amount', 'status')
    search_fields = ('user__username', 'order__id')
    list_filter = ('status',)


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'refund_amount', 'status')
    search_fields = ('user__username', 'order__id')
    list_filter = ('status',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title',)
