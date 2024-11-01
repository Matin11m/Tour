import random
from faker import Faker
from django.core.management.base import BaseCommand
from Tour.models import User, UserProfile, Province, City, Category, Tour, Trip, Favorite, Comment, Passenger, Order, \
    Transaction, Refund

fake = Faker()

# لیست استان‌ها و شهرها
provinces = [
    'تهران', 'فارس', 'خراسان رضوی', 'اصفهان', 'آذربایجان شرقی',
    'آذربایجان غربی', 'گیلان', 'مازندران', 'هرمزگان', 'سیستان و بلوچستان',
    'کرمان', 'لرستان', 'خوزستان', 'همدان', 'زنجان', 'قم',
]

cities = {
    'تهران': ['تهران', 'ری', 'شمیرانات', 'پیشوا'],
    'فارس': ['شیراز', 'مرودشت', 'جهرم', 'کازرون'],
    'خراسان رضوی': ['مشهد', 'نیشابور', 'سبزوار', 'تربت حیدریه'],
    'اصفهان': ['اصفهان', 'کاشان', 'نطنز', 'نجف آباد'],
    'آذربایجان شرقی': ['تبریز', 'مراغه', 'خوی', 'بناب'],
    'آذربایجان غربی': ['ارومیه', 'مهاباد', 'خوی', 'سردشت'],
    'گیلان': ['رشت', 'لاهیجان', 'آستارا', 'تالش'],
    'مازندران': ['ساری', 'آمل', 'بابل', 'تنکابن'],
    'هرمزگان': ['بندرعباس', 'قشم', 'میناب', 'زنجیره'],
    'سیستان و بلوچستان': ['زاهدان', 'زابل', 'خاش', 'سراوان'],
    'کرمان': ['کرمان', 'رفسنجان', 'بم', 'زرند'],
    'لرستان': ['خرم‌آباد', 'بروجرد', 'الشتر', 'دورود'],
    'خوزستان': ['اهواز', 'خرمشهر', 'اندیمشک', 'شوش'],
    'همدان': ['همدان', 'ملایر', 'نهاوند', 'تویسرکان'],
    'زنجان': ['زنجان', 'خرمدره', 'ابهر', 'ماه‌نشان'],
    'قم': ['قم', 'کهک', 'قنوات', 'دستجرد'],
}


class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **options):
        # پاک کردن داده‌های قدیمی
        self.clean_database()

        # ایجاد داده‌های جدید
        self.create_provinces()
        self.create_cities()

        # ایجاد کاربران و پروفایل‌ها
        users = self.create_users(10)
        self.create_user_profiles(users)  # ایجاد پروفایل برای کاربران

        # ایجاد دسته‌بندی‌ها
        categories = self.create_categories(5)

        # دریافت لیست نمونه‌های City
        city_instances = list(City.objects.all())  # اطمینان از اینکه لیستی از اشیاء City دارید

        # ایجاد تورها
        tours = self.create_tours(categories, city_instances, 30)

        # ایجاد سفرها، علاقمندی‌ها و نظرات
        self.create_trips(tours, 50)
        self.create_favorites(users, tours, 20)
        self.create_comments(users, tours, 30)

        # دریافت لیست سفرها برای ایجاد سفارشات
        trips = list(Trip.objects.all())  # دریافت تمام سفرها
        passengers = self.create_passengers(users, 50)  # ایجاد مسافران

        # ایجاد سفارشات، تراکنش‌ها و بازپرداخت‌ها
        orders = self.create_orders(users, trips, passengers, 30)  # ارسال passengers به create_orders
        transactions = self.create_transactions(orders, 30)
        self.create_refunds(transactions, 10)

        self.stdout.write(self.style.SUCCESS('Data populated successfully.'))

    def clean_database(self):
        # پاک‌سازی تمامی داده‌ها از مدل‌ها
        Refund.objects.all().delete()
        Transaction.objects.all().delete()
        Order.objects.all().delete()
        Favorite.objects.all().delete()
        Comment.objects.all().delete()
        Passenger.objects.all().delete()
        Tour.objects.all().delete()
        Trip.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()  # پاک‌سازی کاربران
        City.objects.all().delete()
        Province.objects.all().delete()

    def create_provinces(self):
        for province_name in provinces:
            Province.objects.get_or_create(name=province_name)

    def create_cities(self):
        for province_name, city_names in cities.items():
            province, _ = Province.objects.get_or_create(name=province_name)
            for city_name in city_names:
                City.objects.get_or_create(name=city_name, province=province)

    def create_users(self, num_users):
        users = []
        for _ in range(num_users):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password',
                email=fake.email()
            )
            users.append(user)
        return users

    def create_user_profiles(self, users):
        for user in users:
            UserProfile.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                national_id=fake.random_int(min=1000000000, max=9999999999),
                birth_date=fake.date_of_birth(),
                gender=random.choice(['male', 'female']),
                marital_status=random.choice(['single', 'married']),
                card_number=fake.random_int(min=1000000000000000, max=9999999999999999),
                iban=fake.bban()
            )

    def create_categories(self, num_categories):
        categories = []
        for _ in range(num_categories):
            category = Category.objects.create(
                title=fake.word(),
                description=fake.text()
            )
            categories.append(category)
        return categories

    def create_tours(self, categories, cities, num_tours):
        tours = []
        for _ in range(num_tours):
            city_instance = random.choice(cities)  # انتخاب یک شیء City به صورت تصادفی
            tour = Tour.objects.create(
                category=random.choice(categories),
                city=city_instance,  # استفاده از نمونه City
                title=fake.sentence(),
                description=fake.text(),
                transport=fake.word(),
                stay=fake.word(),
                details=fake.text()
            )
            tours.append(tour)
        return tours

    def create_trips(self, tours, num_trips):
        for _ in range(num_trips):
            trip = Trip.objects.create(
                tour=random.choice(tours),
                price=fake.random_int(min=100000, max=1000000),
                discount_price=fake.random_int(min=50000, max=900000),
                capacity=fake.random_int(min=1, max=50),
                start_date=fake.date(),
                end_date=fake.date(),
                meal=fake.word()
            )

    def create_favorites(self, users, tours, num_favorites):
        for _ in range(num_favorites):
            Favorite.objects.create(
                user=random.choice(users),
                tour=random.choice(tours)
            )

    def create_comments(self, users, tours, num_comments):
        for _ in range(num_comments):
            Comment.objects.create(
                text=fake.text(),
                user=random.choice(users),
                tour=random.choice(tours),
                score=fake.random_int(min=1, max=5),
                visibility=random.choice(['pending', 'approved', 'rejected'])
            )

    def create_orders(self, users, trips, passengers, num_orders):
        orders = []
        for _ in range(num_orders):
            order = Order.objects.create(
                user=random.choice(users),
                passenger=random.choice(passengers),  # انتخاب تصادفی مسافر
                trip=random.choice(trips),  # انتخاب تصادفی سفر
                price=fake.random_int(min=100000, max=1000000),
                adults_number=fake.random_int(min=1, max=5),  # تعداد بزرگسالان
                children_number=fake.random_int(min=0, max=3),  # تعداد کودکان
                order_status='pending',  # وضعیت سفارش
                payment_status='unpaid',  # وضعیت پرداخت
                refund_status='not_requested'  # وضعیت بازپرداخت
            )
            orders.append(order)
        return orders

    def create_transactions(self, orders, num_transactions):
        transactions = []
        for _ in range(num_transactions):
            transaction = Transaction.objects.create(
                user=random.choice(orders).user,  # انتخاب تصادفی یک کاربر از سفارش
                order=random.choice(orders),  # انتخاب تصادفی یک سفارش
                amount=fake.random_int(min=100000, max=1000000),  # مقدار تصادفی برای مبلغ
                status=random.choice(['success', 'pending', 'failed']),  # وضعیت تصادفی
            )
            transactions.append(transaction)
        return transactions

    def create_refunds(self, transactions, num_refunds):
        for _ in range(num_refunds):
            transaction = random.choice(transactions)  # انتخاب تصادفی یک معامله
            Refund.objects.create(
                user=transaction.user,  # کاربر را از معامله انتخاب کنید
                order=transaction.order,  # سفارش را از معامله انتخاب کنید
                text=fake.sentence(),  # متن بازپرداخت به صورت تصادفی
                refund_amount=round(transaction.amount * random.uniform(0.1, 1.0), 2),  # مقدار بازپرداخت تصادفی
                status=random.choice(['requested', 'approved', 'denied'])  # وضعیت تصادفی
            )

    def create_passengers(self, users, num_passengers):
        passengers = []  # لیستی برای نگهداری مسافران
        for _ in range(num_passengers):
            passenger = Passenger.objects.create(
                user=random.choice(users),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                national_id=fake.random_int(min=1000000000, max=9999999999),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),  # برای سنین بالای 18 سال
                gender=random.choice(['male', 'female'])  # انتخاب تصادفی جنسیت
            )
            passengers.append(passenger)  # اضافه کردن مسافر به لیست
        return passengers  # بازگرداندن لیست مسافران
