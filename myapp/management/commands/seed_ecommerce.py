from django.core.management.base import BaseCommand
from myapp.models import Category, Product, Review
from django.contrib.auth.models import User
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = "Seed database with premium Bangladeshi e-commerce data (Product Focus)"

    def handle(self, *args, **kwargs):
        # 1. Clear old data
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        # 2. Create categories
        cats_data = [
            ("Premium Panjabi", "Traditional menswear and fabrics"),
            ("Local Organic Food", "Honey, Ghee and organic snacks"),
            ("Handicrafts", "Nakshi Kantha and traditional decor"),
            ("Digital Assets", "Premium Website Templates and scripts"),
            ("Gadgets", "Top tier electronics and accessories"),
        ]
        
        categories = {}
        for name, desc in cats_data:
            cat, _ = Category.objects.get_or_create(
                name=name, 
                defaults={'slug': slugify(name), 'description': desc}
            )
            categories[name] = cat
            
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} categories"))

        # 3. Create products (Using product-only still life images)
        products_data = [
            # Premium Panjabi (Focus on fabric/folded shots)
            ("Royal White Silk Panjabi", 4500, "Premium Panjabi", "https://images.unsplash.com/photo-1597983073493-88cd35cf93b0?w=500&q=80"),
            ("Designer Cotton Panjabi", 2800, "Premium Panjabi", "https://images.unsplash.com/photo-1621335829175-95f437384d7c?w=500&q=80"),
            ("Black Premium Kabli Set", 5500, "Premium Panjabi", "https://images.unsplash.com/photo-1589310243389-96a5483213a8?w=500&q=80"),
            
            # Local Organic Food
            ("Sundarban Pure Honey (1kg)", 1200, "Local Organic Food", "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=500&q=80"),
            ("Pure Deshi Ghee (500g)", 950, "Local Organic Food", "https://images.unsplash.com/photo-1589927986089-35812388d1f4?w=500&q=80"),
            
            # Handicrafts
            ("Nakshi Kantha Wall Hanging", 4500, "Handicrafts", "https://images.unsplash.com/photo-1590013332441-9f673e4837cd?w=500&q=80"),
            ("Jute Craft Table Runner", 1500, "Handicrafts", "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=500&q=80"),
            
            # Digital Assets
            ("E-Commerce Website Template", 25000, "Digital Assets", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500&q=80"),
            ("Business Portfolio Site", 15000, "Digital Assets", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=500&q=80"),
            ("News Portal Full Script", 45000, "Digital Assets", "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=500&q=80"),
            
            # Gadgets
            ("Premium Noise Cancelling Buds", 5500, "Gadgets", "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&q=80"),
        ]

        products = []
        for name, price, cat_name, img in products_data:
            cat = categories[cat_name]
            p, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': f"Premium {name} sourced directly from the finest artisans of Bangladesh. Quality guaranteed.",
                    'price': price,
                    'stock': random.randint(10, 100),
                    'category': cat,
                    'image_url': img
                }
            )
            products.append(p)

        self.stdout.write(self.style.SUCCESS(f"Created {len(products)} products"))

        # 4. Create reviews
        admin = User.objects.filter(is_superuser=True).first()
        if admin:
            comments = [
                "অসাধারণ কোয়ালিটি! অনেক ধন্যবাদ।",
                "খুবই ভালো সার্ভিস, ডেলিভারিও তাড়াতাড়ি হয়েছে।",
                "পণ্যের মান অনেক উন্নত।",
                "ঠিক যেমনটি চেয়েছিলাম, তেমনই পেয়েছি।",
                "বেস্ট ডিল! রেকমেন্ড করছি সবাইকে।"
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
            self.stdout.write(self.style.SUCCESS("Added local language reviews"))
