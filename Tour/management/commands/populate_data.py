# import random
#
# from django.contrib.auth.models import User
# from django.core.management.base import BaseCommand
# from faker import Faker
# from Tour.models import UserProfile, City, Category, Tour, Trip, Order, Transaction, Refund, Comment, \
#     Favorite, CityBanner, FirstBanner, Banner, Passenger
#
#
# class Command(BaseCommand):
#     help = 'Generates fake data for the travel system'
#
#     def handle(self, *args, **kwargs):
#         fake = Faker('fa_IR')  # زبان فارسی
#
#         # پاکسازی داده‌های قبلی
#         self.clear_old_data()
#
#         # کاهش تعداد داده‌ها (ایجاد 5 نمونه)
#         self.create_provinces_and_cities(fake, num=5)
#         self.create_categories(fake, num=3)
#         self.create_tours_and_trips(fake, num=5)
#         self.create_users_and_orders(fake, num=5)
#         self.create_transactions(fake, num=5)
#         self.create_refunds(fake, num=5)
#         self.create_banners(fake, num=3)
#         self.create_city_banners(fake, num=3)
#         self.create_first_banners(fake, num=3)
#         self.create_favorites(fake, num=3)
#         self.create_comments(fake, num=5)
#
#         self.stdout.write(self.style.SUCCESS('Fake data created successfully!'))
#
#     def clear_old_data(self):
#         # پاکسازی داده‌ها از جداول مختلف
#         UserProfile.objects.all().delete()
#         User.objects.all().delete()
#         City.objects.all().delete()
#         Category.objects.all().delete()
#         Tour.objects.all().delete()
#         Trip.objects.all().delete()
#         Order.objects.all().delete()
#         Transaction.objects.all().delete()
#         Refund.objects.all().delete()
#         Comment.objects.all().delete()
#         Favorite.objects.all().delete()
#         CityBanner.objects.all().delete()
#         FirstBanner.objects.all().delete()
#         Banner.objects.all().delete()
#
#     def create_provinces_and_cities(self, fake, num):
#         provinces = ['تهران', 'اصفهان', 'شیراز', 'مشهد', 'تبریز']
#         cities = {
#             'تهران': ['تهران', 'ورامین', 'کرج'],
#             'اصفهان': ['اصفهان', 'کاشان', 'نطنز'],
#             'شیراز': ['شیراز', 'مرودشت', 'کازرون'],
#             'مشهد': ['مشهد', 'تربت حیدریه', 'چناران'],
#             'تبریز': ['تبریز', 'مراغه', 'مقدم']
#         }
#
#         for cities_list in cities.values():
#             for city_name in cities_list:
#                 City.objects.create(name=city_name)
#
#     def create_categories(self, fake, num):
#         categories = ['تورهای داخلی', 'تورهای خارجی', 'تورهای ویژه', 'تورهای طبیعت گردی']
#         for category in categories:
#             Category.objects.create(title=category, description=fake.text(), image=None)
#
#     def create_tours_and_trips(self, fake, num):
#         categories = Category.objects.all()
#         cities = City.objects.all()
#         for category in categories:
#             for _ in range(5):
#                 city = random.choice(cities)
#                 tour = Tour.objects.create(
#                     category=category,
#                     city=city,
#                     title=fake.company(),
#                     description=fake.text(),
#                     stay=fake.word(),
#                     details=fake.text(),
#                     tour_rules=fake.text(),
#                     required_documents=fake.text(),
#                     image=None
#                 )
#                 self.create_trips_for_tour(tour, fake)
#
#     def create_trips_for_tour(self, tour, fake):
#         for _ in range(3):
#             Trip.objects.create(
#                 tour=tour,
#                 price=random.randint(1000000, 5000000),
#                 discount_price=random.randint(500000, 3000000) if random.random() > 0.5 else None,
#                 capacity=random.randint(10, 50),
#                 duration=fake.word(),
#                 stay=fake.word(),
#                 trip_type=fake.word(),
#                 start_date=fake.date_this_year(),
#                 end_date=fake.date_this_year(),
#                 meal=fake.word()
#             )
#
#     def create_users_and_orders(self, fake, num):
#         for _ in range(num):  # تعداد کاربران مورد نظر
#             # ابتدا یک کاربر جدید در مدل User ایجاد می‌کنیم
#             user = User.objects.create_user(
#                 username=fake.user_name(),
#                 email=fake.email(),
#                 password='password123'
#             )
#
#             # ایجاد پروفایل کاربر مرتبط با کاربر جدید
#             user_profile = UserProfile.objects.create(
#                 user=user,
#                 first_name=fake.first_name(),
#                 last_name=fake.last_name(),
#                 phone_number=fake.phone_number(),
#                 phone_number_emergency=fake.phone_number(),
#                 national_id=fake.random_number(digits=10, fix_len=True),
#                 birth_date=fake.date_of_birth(),
#                 gender=random.choice(['male', 'female']),
#                 marital_status=random.choice(['single', 'married']),
#                 card_number=fake.random_number(digits=16, fix_len=True),
#                 iban=fake.random_number(digits=24, fix_len=True)
#             )
#
#             # ایجاد یک مسافر جدید
#             passenger = Passenger.objects.create(
#                 user=user,
#                 first_name=fake.first_name(),
#                 last_name=fake.last_name(),
#                 national_id=fake.ssn(),  # یا می‌توانید از یک عدد تصادفی استفاده کنید
#                 birth_date=fake.date_of_birth(),
#                 gender=fake.random_element(['male', 'female'])
#             )
#
#             self.stdout.write(
#                 self.style.SUCCESS(f'Passenger "{passenger.first_name} {passenger.last_name}" created successfully'))
#             # انتخاب یک سفر تصادفی از جدول Trip
#             trip = random.choice(Trip.objects.all())
#
#             # ایجاد نمونه Order
#             order = Order.objects.create(
#                 passenger=passenger,
#                 user=user,
#                 trip=trip,
#                 price=round(random.uniform(100, 1000), 2),  # قیمت تصادفی
#                 adults_number=random.randint(1, 5),  # تعداد بزرگسالان تصادفی
#                 children_number=random.randint(0, 3),  # تعداد کودکان تصادفی
#                 order_status=random.choice(['pending', 'confirmed', 'cancelled']),
#                 payment_status=random.choice(['paid', 'unpaid']),
#                 refund_status=random.choice(['not_requested', 'requested', 'refunded']),
#             )
#
#             self.stdout.write(self.style.SUCCESS(f'Successfully created order for {user.username}'))
#
#             # ایجاد نمونه Transaction
#             Transaction.objects.create(
#                 user=user,
#                 order=order,
#                 amount=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
#                 transaction_details=fake.text(),
#                 status="completed"
#             )
#
#             # ایجاد نمونه Refund
#             Refund.objects.create(
#                 user=user,
#                 order=order,
#                 text=fake.text(),
#                 refund_amount=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
#                 status="requested"
#             )
#
#             # ایجاد نمونه Comment
#             Comment.objects.create(
#                 text=fake.text(),
#                 user=user,
#                 tour=trip.tour,  # مقدار tour مرتبط با trip
#                 score=fake.random_int(min=1, max=5),
#                 visibility="approved"
#             )
#
#     def create_orders_for_user(self, user, fake, num):
#         trips = Trip.objects.all()
#         for _ in range(2):  # هر کاربر دو سفارش ایجاد می‌کند
#             trip = random.choice(trips)
#             Order.objects.create(
#                 passenger=user,
#                 user=user.user,
#                 trip=trip,
#                 price=trip.price,
#                 adults_number=random.randint(1, 3),
#                 children_number=random.randint(0, 2),
#                 order_status=random.choice(['pending', 'confirmed', 'canceled']),
#                 payment_status=random.choice(['paid', 'unpaid']),
#                 refund_status=random.choice(['not_requested', 'requested', 'approved'])
#             )
#
#     def create_comments(self, fake, num):
#         tours = Tour.objects.all()
#         users = UserProfile.objects.all()
#         for tour in tours:
#             for _ in range(3):
#                 Comment.objects.create(
#                     text=fake.text(),
#                     user=random.choice(users),
#                     tour=tour,
#                     score=random.randint(1, 5),
#                     visibility=random.choice(['pending', 'approved', 'rejected'])
#                 )
#
#     def create_transactions(self, fake, num):
#         orders = Order.objects.all()
#         for order in orders:
#             Transaction.objects.create(
#                 user=order.user,
#                 order=order,
#                 amount=order.price,
#                 transaction_details=fake.text(),
#                 status=random.choice(['pending', 'completed', 'failed'])
#             )
#
#     def create_refunds(self, fake, num):
#         orders = Order.objects.filter(payment_status='paid')
#         for order in orders:
#             Refund.objects.create(
#                 user=order.user,
#                 order=order,
#                 text=fake.text(),
#                 refund_amount=random.uniform(500000, float(order.price)),
#                 status=random.choice(['requested', 'approved', 'rejected'])
#             )
#
#     def create_banners(self, fake, num):
#         for _ in range(5):
#             Banner.objects.create(
#                 title=fake.company(),
#                 image=None,  # برای تست، می‌توانید مسیر فایل‌های واقعی را جایگزین کنید.
#                 link=fake.url(),
#
#             )
#
#     def create_first_banners(self, fake, num):
#         categories = Category.objects.all()
#         for category in categories:
#             FirstBanner.objects.create(
#                 title=fake.company(),
#                 image=None,  # مسیر تصویر فیک
#                 category=category
#             )
#
#     def create_city_banners(self, fake, num):
#         cities = City.objects.all()
#         for city in cities:
#             CityBanner.objects.create(
#                 title=fake.city(),
#                 image=None,  # مسیر تصویر فیک
#                 city=city
#             )
#
#     def create_favorites(self, fake, num):
#         users = UserProfile.objects.all()
#         tours = Tour.objects.all()
#         for user in users:
#             favorite_tours = random.sample(list(tours), k=random.randint(1, 5))
#             for tour in favorite_tours:
#                 Favorite.objects.create(user=user.user, tour=tour)
#
#     def create_comments(self, fake, num):
#         tours = Tour.objects.all()
#         users = UserProfile.objects.all()
#         for tour in tours:
#             for _ in range(3):  # سه نظر برای هر تور
#                 Comment.objects.create(
#                     text=fake.text(),
#                     user=random.choice(users).user,
#                     tour=tour,
#                     score=random.randint(1, 5),
#                     visibility=random.choice(['pending', 'approved', 'rejected'])
#                 )


import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from Tour.models import UserProfile, City, Category, Tour, Trip, Order, Transaction, Refund, Comment, \
    Favorite, CityBanner, FirstBanner, Banner, Passenger


class Command(BaseCommand):
    help = 'Generates fake data for the travel system'

    def handle(self, *args, **kwargs):
        fake = Faker('fa_IR')  # زبان فارسی
        City.objects.filter(province__isnull=True).delete()

        # پاکسازی داده‌های قبلی
        self.clear_old_data()

        # ایجاد داده‌ها
        self.create_cities(fake, num=5)  # ایجاد داده‌ها برای شهرها
        self.create_categories(fake, num=3)  # ایجاد دسته‌بندی‌ها
        self.create_tours_and_trips(fake, num=5)  # ایجاد تورها و سفرها
        self.create_users_and_orders(fake, num=5)  # ایجاد کاربران و سفارش‌ها
        self.create_transactions(fake, num=5)  # ایجاد تراکنش‌ها
        self.create_refunds(fake, num=5)  # ایجاد درخواست‌های بازگشت وجه
        self.create_banners(fake, num=3)  # ایجاد بنرها
        self.create_city_banners(fake, num=3)  # ایجاد بنرهای شهری
        self.create_first_banners(fake, num=3)  # ایجاد بنرهای اولیه
        self.create_favorites(fake, num=3)  # ایجاد لیست‌های علاقه‌مندی
        self.create_comments(fake, num=5)  # ایجاد نظرات
        self.create_passengers(fake, num=5)  # ایجاد مسافران

        self.stdout.write(self.style.SUCCESS('Fake data created successfully!'))

    def clear_old_data(self):
        # پاکسازی داده‌ها از جداول مختلف
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        City.objects.all().delete()
        Category.objects.all().delete()
        Tour.objects.all().delete()
        Trip.objects.all().delete()
        Order.objects.all().delete()
        Transaction.objects.all().delete()
        Refund.objects.all().delete()
        Comment.objects.all().delete()
        Favorite.objects.all().delete()
        CityBanner.objects.all().delete()
        FirstBanner.objects.all().delete()
        Banner.objects.all().delete()
        Passenger.objects.all().delete()

    def create_cities(self, fake, num):
        # تعریف لیستی از نام‌های شهرها
        cities = ['تهران', 'اصفهان', 'شیراز', 'مشهد', 'تبریز']
        for city_name in cities:
            City.objects.create(name=city_name)

    def create_categories(self, fake, num):
        categories = ['تورهای داخلی', 'تورهای خارجی', 'تورهای ویژه', 'تورهای طبیعت گردی']
        for category in categories:
            Category.objects.create(title=category, description=fake.text(), image=None)

    def create_tours_and_trips(self, fake, num):
        categories = Category.objects.all()
        cities = City.objects.all()
        for category in categories:
            for _ in range(5):
                city = random.choice(cities)
                tour = Tour.objects.create(
                    category=category,
                    city=city,
                    title=fake.company(),
                    description=fake.text(),
                    stay=fake.word(),
                    details=fake.text(),
                    tour_rules=fake.text(),
                    required_documents=fake.text(),
                    image=None
                )
                self.create_trips_for_tour(tour, fake)

    def create_trips_for_tour(self, tour, fake):
        for _ in range(3):
            Trip.objects.create(
                tour=tour,
                price=random.randint(1000000, 5000000),
                discount_price=random.randint(500000, 3000000) if random.random() > 0.5 else None,
                capacity=random.randint(10, 50),
                duration=fake.word(),
                stay=fake.word(),
                trip_type=fake.word(),
                start_date=fake.date_this_year(),
                end_date=fake.date_this_year(),
                meal=fake.word()
            )

    def create_users_and_orders(self, fake, num):
        for _ in range(num):  # تعداد کاربران مورد نظر
            # ایجاد کاربر جدید
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )

            # ایجاد پروفایل کاربر
            user_profile = UserProfile.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                phone_number_emergency=fake.phone_number(),
                national_id=fake.random_number(digits=10, fix_len=True),
                birth_date=fake.date_of_birth(),
                gender=random.choice(['male', 'female']),
                marital_status=random.choice(['single', 'married']),
                card_number=fake.random_number(digits=16, fix_len=True),
                iban=fake.random_number(digits=24, fix_len=True)
            )

            # ایجاد مسافر
            passenger = Passenger.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                national_id=fake.ssn(),  # یا می‌توانید از یک عدد تصادفی استفاده کنید
                birth_date=fake.date_of_birth(),
                gender=fake.random_element(['male', 'female'])
            )

            # انتخاب یک سفر تصادفی
            trip = random.choice(Trip.objects.all())

            # ایجاد سفارش
            order = Order.objects.create(
                passenger=passenger,
                user=user,
                trip=trip,
                price=round(random.uniform(100, 1000), 2),
                adults_number=random.randint(1, 5),
                children_number=random.randint(0, 3),
                order_status=random.choice(['pending', 'confirmed', 'cancelled']),
                payment_status=random.choice(['paid', 'unpaid']),
                refund_status=random.choice(['not_requested', 'requested', 'refunded']),
            )

            # ایجاد تراکنش
            Transaction.objects.create(
                user=user,
                order=order,
                amount=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                transaction_details=fake.text(),
                status="completed"
            )

            # ایجاد درخواست بازگشت وجه
            Refund.objects.create(
                user=user,
                order=order,
                text=fake.text(),
                refund_amount=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                status="requested"
            )

            # ایجاد نظر (Comment)
            Comment.objects.create(
                text=fake.text(),
                user=user,
                tour=trip.tour,  # مقدار tour مرتبط با trip
                score=fake.random_int(min=1, max=5),
                visibility="approved"
            )

    def create_banners(self, fake, num):
        # ایجاد بنرهای عمومی
        for _ in range(num):
            Banner.objects.create(
                title=fake.sentence(),  # عنوان بنر
                image=None  # آدرس تصویر فیک یا مسیر دلخواه
            )

    def create_city_banners(self, fake, num):
        # بنرهای مخصوص شهرها را ایجاد می‌کند
        cities = City.objects.all()
        for _ in range(num):
            city_banner = CityBanner.objects.create(
                city=random.choice(cities),
                title=fake.company(),
                image=None
            )

    def create_first_banners(self, fake, num):
        # ایجاد بنرهای اولیه
        categories = Category.objects.all()  # دسترسی به دسته‌ها
        for _ in range(num):
            # ایجاد بنر اولیه با اطلاعات فیک
            category = random.choice(categories)  # انتخاب یک دسته تصادفی از دسته‌ها
            FirstBanner.objects.create(
                title=fake.sentence(),  # عنوان بنر
                image=None,  # در صورت نیاز، می‌توانید یک تصویر فیک قرار دهید
                category=category  # انتخاب یک دسته تصادفی
            )

    def create_favorites(self, fake, num):
        # ایجاد لیست علاقه‌مندی‌ها
        users = User.objects.all()
        tours = Tour.objects.all()
        for _ in range(num):
            user = random.choice(users)  # انتخاب یک کاربر تصادفی
            tour = random.choice(tours)  # انتخاب یک تور تصادفی
            Favorite.objects.create(
                user=user,
                tour=tour
            )

    def create_comments(self, fake, num):
        # نظرات مختلف را ایجاد می‌کند
        users = User.objects.all()
        tours = Tour.objects.all()
        for _ in range(num):
            Comment.objects.create(
                text=fake.text(),
                user=random.choice(users),
                tour=random.choice(tours),
                score=fake.random_int(min=1, max=5),
                visibility="approved"
            )

    def create_passengers(self, fake, num):
        # ایجاد مسافران
        users = User.objects.all()
        for _ in range(num):
            user = random.choice(users)  # انتخاب یک کاربر تصادفی
            Passenger.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                national_id=fake.ssn(),  # یا از شماره ملی تصادفی می‌توانید استفاده کنید
                birth_date=fake.date_of_birth(),
                gender=fake.random_element(['male', 'female'])
            )

    def create_transactions(self, fake, num):
        # ایجاد تراکنش‌ها
        for _ in range(num):
            order = random.choice(Order.objects.all())  # انتخاب یک سفارش تصادفی
            Transaction.objects.create(
                user=order.user,
                order=order,
                amount=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                transaction_details=fake.text(),
                status="completed"
            )

    def create_refunds(self, fake, num):
        # ایجاد درخواست‌های بازگشت وجه
        for _ in range(num):
            order = random.choice(Order.objects.all())  # انتخاب یک سفارش تصادفی
            Refund.objects.create(
                user=order.user,
                order=order,
                text=fake.text(),
                refund_amount=fake.pydecimal(left_digits=5, right_digits=2, positive=True),
                status=random.choice(['requested', 'approved', 'rejected'])
            )
