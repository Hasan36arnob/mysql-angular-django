from django.core.management.base import BaseCommand
from myapp.models import Category, Product, Review
from django.contrib.auth.models import User
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = "Seed database with sample e-commerce data"

    def handle(self, *args, **kwargs):
        # 1. Create categories
        cats_data = [
            ("Electronics", "Gadgets, devices and more"),
            ("Clothing", "Trendy fashion for everyone"),
            ("Home & Kitchen", "Make your home beautiful"),
            ("Books", "Knowledge and entertainment"),
            ("Sports", "Gear for your favorite activities"),
        ]
        
        categories = []
        for name, desc in cats_data:
            cat, _ = Category.objects.get_or_create(
                name=name, 
                defaults={'slug': slugify(name), 'description': desc}
            )
            categories.append(cat)
            
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} categories"))

        # 2. Create products
        products_data = [
            ("Premium Wireless Headphones", 199.99, "Electronics", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"),
            ("Modern Smartwatch", 249.50, "Electronics", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"),
            ("Cotton T-Shirt", 25.00, "Clothing", "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&q=80"),
            ("Denim Jacket", 89.00, "Clothing", "https://images.unsplash.com/photo-1523206489230-c012c64b2b48?w=500&q=80"),
            ("Chef's Knife Set", 120.00, "Home & Kitchen", "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&q=80"),
            ("Eco-friendly Yoga Mat", 45.00, "Sports", "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=500&q=80"),
            ("Professional DSLR Camera", 1200.00, "Electronics", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&q=80"),
            ("Leather Messenger Bag", 150.00, "Clothing", "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500&q=80"),
            ("Minimalist Wall Clock", 35.00, "Home & Kitchen", "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=500&q=80"),
            ("The Art of Programming", 55.00, "Books", "https://images.unsplash.com/photo-1512428559087-560fa5ceab42?w=500&q=80"),
        ]

        products = []
        for name, price, cat_name, img in products_data:
            cat = Category.objects.get(name=cat_name)
            p, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': f"High quality {name} from our {cat_name} collection.",
                    'price': price,
                    'stock': random.randint(5, 50),
                    'category': cat,
                    'image_url': img
                }
            )
            products.append(p)

        self.stdout.write(self.style.SUCCESS(f"Created {len(products)} products"))

        # 3. Create reviews (if user admin exists)
        admin = User.objects.filter(is_superuser=True).first()
        if admin:
            comments = [
                "Excellent quality, highly recommended!",
                "Good value for money.",
                "Fast shipping and great service.",
                "Exactly as described.",
                "A bit expensive but worth it."
            ]
            for p in products:
                Review.objects.get_or_create(
                    user=admin,
                    product=p,
                    defaults={
                        'rating': random.randint(4, 5),
                        'comment': random.choice(comments)
                    }
                )
            self.stdout.write(self.style.SUCCESS("Added sample reviews"))
