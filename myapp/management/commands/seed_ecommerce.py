from django.core.management.base import BaseCommand
from myapp.models import Category, Product, Review
from django.contrib.auth.models import User
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = "Seed database with a massive collection of premium Bangladeshi products"

    def handle(self, *args, **kwargs):
        # 1. Clear old data
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        # 2. Define Categories
        cats_data = [
            ("Premium Panjabi", "Exquisite menswear from top artisans"),
            ("Traditional Kabli", "Classic and modern Kabli sets"),
            ("Organic Food", "Pure and authentic local flavors"),
            ("Handicrafts", "Hand-made masterpieces of Bengal"),
            ("Digital Assets", "High-end website templates and code"),
            ("Tech Gadgets", "Modern electronics and accessories"),
            ("Home Decor", "Traditional aesthetics for your home"),
            ("Luxury Perfumes", "Exotic local and imported fragrances"),
        ]
        
        categories = {}
        for name, desc in cats_data:
            cat, _ = Category.objects.get_or_create(
                name=name, 
                defaults={'slug': slugify(name), 'description': desc}
            )
            categories[name] = cat
            
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} premium categories"))

        # 3. Define a massive product list (40+ items)
        products_data = [
            # --- Premium Panjabi ---
            ("Royal White Silk Panjabi", 12500, "Premium Panjabi", "https://images.unsplash.com/photo-1597983073493-88cd35cf93b0?w=500&q=80"),
            ("Midnight Black Designer Panjabi", 8500, "Premium Panjabi", "https://images.unsplash.com/photo-1621335829175-95f437384d7c?w=500&q=80"),
            ("Embroidered Maroon Silk Panjabi", 15000, "Premium Panjabi", "https://images.unsplash.com/photo-1589310243389-96a5483213a8?w=500&q=80"),
            ("Golden Tussar Silk Panjabi", 18500, "Premium Panjabi", "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=500&q=80"),
            ("Hand-loomed Cotton Panjabi", 3500, "Premium Panjabi", "https://images.unsplash.com/photo-1594932224828-b4b057b7d6ee?w=500&q=80"),
            ("Azure Blue Slim-fit Panjabi", 4200, "Premium Panjabi", "https://images.unsplash.com/photo-1617137968427-85924c800a22?w=500&q=80"),

            # --- Traditional Kabli ---
            ("Peshawari Design Kabli Set", 6500, "Traditional Kabli", "https://images.unsplash.com/photo-1598411037848-00530cc39615?w=500&q=80"),
            ("Modern Navy Blue Kabli", 7200, "Traditional Kabli", "https://images.unsplash.com/photo-1590035221029-4421e19d5181?w=500&q=80"),
            ("Charcoal Grey Kabli Suite", 8000, "Traditional Kabli", "https://images.unsplash.com/photo-1593030761757-71fae45fa0e7?w=500&q=80"),
            ("Off-white Festive Kabli", 5800, "Traditional Kabli", "https://images.unsplash.com/photo-1590035221029-4421e19d5181?w=500&q=80"),

            # --- Organic Food ---
            ("Sundarban Lichi Honey (1kg)", 1500, "Organic Food", "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=500&q=80"),
            ("Pure Deshi Cow Ghee (500g)", 1100, "Organic Food", "https://images.unsplash.com/photo-1589927986089-35812388d1f4?w=500&q=80"),
            ("Premium Kalijeera Rice (5kg)", 850, "Organic Food", "https://images.unsplash.com/photo-1586201327693-866199f1417f?w=500&q=80"),
            ("Organic Turmeric Powder (250g)", 250, "Organic Food", "https://images.unsplash.com/photo-1615485242231-82abb2f1f0d0?w=500&q=80"),
            ("Cold Pressed Mustard Oil (1L)", 450, "Organic Food", "https://images.unsplash.com/photo-1474979266404-7eaacfb88c51?w=500&q=80"),
            ("Hand-picked Tea Leaves (Srimangal)", 600, "Organic Food", "https://images.unsplash.com/photo-1544787210-2213d64ad9ff?w=500&q=80"),

            # --- Handicrafts ---
            ("Nakshi Kantha Hand-stitched", 12000, "Handicrafts", "https://images.unsplash.com/photo-1590013332441-9f673e4837cd?w=500&q=80"),
            ("Jute Craft Table Runner", 1800, "Handicrafts", "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=500&q=80"),
            ("Traditional Pottery Set (12pc)", 4500, "Handicrafts", "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=500&q=80"),
            ("Bamboo Hand-woven Basket", 1200, "Handicrafts", "https://images.unsplash.com/photo-1591084728795-1149f32d9866?w=500&q=80"),
            ("Brass Flower Vase (Artisan)", 3200, "Handicrafts", "https://images.unsplash.com/photo-1581781870027-04212e231e96?w=500&q=80"),

            # --- Digital Assets ---
            ("Advanced E-Commerce Script", 55000, "Digital Assets", "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500&q=80"),
            ("Multi-Vendor Marketplace Site", 85000, "Digital Assets", "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500&q=80"),
            ("Portfolio Website React Template", 12000, "Digital Assets", "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=500&q=80"),
            ("School Management ERP", 120000, "Digital Assets", "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=500&q=80"),
            ("News Portal Full Solution", 45000, "Digital Assets", "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=500&q=80"),
            ("Restaurant POS Android App", 35000, "Digital Assets", "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=500&q=80"),

            # --- Tech Gadgets ---
            ("Premium Wireless Buds Gen-3", 6500, "Tech Gadgets", "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&q=80"),
            ("Smart Health Monitor Pro", 12000, "Tech Gadgets", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"),
            ("Mechanical RGB Keyboard", 4500, "Tech Gadgets", "https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500&q=80"),
            ("Gaming Mouse High-Precision", 2800, "Tech Gadgets", "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&q=80"),
            ("USB-C Fast Charging Dock", 3500, "Tech Gadgets", "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=500&q=80"),

            # --- Home Decor ---
            ("Handcrafted Wooden Mirror", 5500, "Home Decor", "https://images.unsplash.com/photo-1618220179428-22790b461013?w=500&q=80"),
            ("Embroidered Cushion Cover Set", 2500, "Home Decor", "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=500&q=80"),
            ("Ceramic Table Lamp Modern", 4200, "Home Decor", "https://images.unsplash.com/photo-1534073828943-f801091bb18c?w=500&q=80"),
            ("Traditional Jute Wall Art", 3800, "Home Decor", "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=500&q=80"),

            # --- Luxury Perfumes ---
            ("Oudh Al-Bakhoor (Exotic)", 9500, "Luxury Perfumes", "https://images.unsplash.com/photo-1541643600914-78b084683601?w=500&q=80"),
            ("Royal Rose Attar (12ml)", 3200, "Luxury Perfumes", "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=500&q=80"),
            ("Midnight Musk Perfume", 5500, "Luxury Perfumes", "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=500&q=80"),
            ("Sandalwood Concentrated Oil", 4800, "Luxury Perfumes", "https://images.unsplash.com/photo-1616948055600-a19116c29957?w=500&q=80"),
        ]

        products = []
        for name, price, cat_name, img in products_data:
            cat = categories[cat_name]
            p, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': f"Premium {name} sourced directly from the finest artisans and creators of Bangladesh. Authenticity and quality are our top priorities.",
                    'price': price,
                    'stock': random.randint(5, 50),
                    'category': cat,
                    'image_url': img
                }
            )
            products.append(p)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(products)} premium products"))

        # 4. Create local language reviews
        admin = User.objects.filter(is_superuser=True).first()
        if admin:
            local_reviews = [
                "অসাধারণ কোয়ালিটি! ঠিক যেমনটা চেয়েছিলাম।",
                "খুবই ভালো সার্ভিস, ডেলিভারিও অনেক তাড়াতাড়ি হয়েছে।",
                "পণ্যের মান অনেক উন্নত এবং ফিনিশিং অসাধারণ।",
                "বেস্ট ডিল! এই দামে এত ভালো পণ্য পাওয়া মুশকিল।",
                "প্যাকেজিং খুব সুন্দর ছিল, ধন্যবাদ বিডি-অ্যামাজন।",
                "এক কথায় চমৎকার! আবারও অর্ডার করব ইনশাআল্লাহ্‌।",
                "খুবই প্রিমিয়াম লুক, সবাইকে রেকমেন্ড করছি।",
                "বিশ্বস্ততার সাথে পণ্যটি কিনতে পারেন।"
            ]
            for p in products:
                # Add 1-3 random reviews per product
                num_reviews = random.randint(1, 3)
                for _ in range(num_reviews):
                    Review.objects.get_or_create(
                        user=admin,
                        product=p,
                        comment=random.choice(local_reviews),
                        defaults={'rating': random.randint(4, 5)}
                    )
            self.stdout.write(self.style.SUCCESS("Added localized premium reviews to all products"))
