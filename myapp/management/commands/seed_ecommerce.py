from django.core.management.base import BaseCommand
from myapp.models import Category, Product, Review
from django.contrib.auth.models import User
from django.utils.text import slugify
import random 

class Command(BaseCommand):
    help = "Seed database with a massive collection of premium Bangladeshi products across multiple categories"

    def handle(self, *args, **kwargs):
        # 1. Clear old data
        Product.objects.all().delete()
        Category.objects.all().delete()
        
        # 2. Define Categories
        cats_data = [
            ("Electronics", "Latest tech, gadgets, and household electronics"),
            ("Fresh Fruits", "Organic, seasonal, and farm-fresh fruits"),
            ("Organic Vegetables", "Chemical-free, healthy vegetables from local farms"),
            ("Books & Stationery", "Best-sellers, educational, and local literature"),
            ("Digital Assets", "High-end website templates and code"),
            ("Home Decor", "Traditional aesthetics for your home"),
            ("Tech Gadgets", "Modern accessories and portable tech"),
        ]
        
        categories = {}
        for name, desc in cats_data:
            cat, _ = Category.objects.get_or_create(
                name=name, 
                defaults={'slug': slugify(name), 'description': desc}
            )
            categories[name] = cat
            
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} premium categories"))

        # 3. Define a massive product list (50+ items)
        products_data = [
            # --- Electronics ---
            ("Ultra Slim 4K Smart TV", 55000, "Electronics", "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=500&q=80"),
            ("Energy-Efficient Refrigerator", 42000, "Electronics", "https://images.unsplash.com/photo-1571175432248-77983678070b?w=500&q=80"),
            ("Automatic Front-Load Washer", 38000, "Electronics", "https://images.unsplash.com/photo-1582735689369-4fe9c757fb44?w=500&q=80"),
            ("Portable Induction Cooktop", 4500, "Electronics", "https://images.unsplash.com/photo-1584990344321-2793ac948a67?w=500&q=80"),
            ("Smart Air Purifier BD Edition", 12000, "Electronics", "https://images.unsplash.com/photo-1585771724684-252ad5058631?w=500&q=80"),
            ("Premium Blender & Mixer", 3200, "Electronics", "https://images.unsplash.com/photo-1570222083775-58742f56018b?w=500&q=80"),

            # --- Fresh Fruits ---
            ("Premium Rajshahi Fazli Mango (5kg)", 1200, "Fresh Fruits", "https://images.unsplash.com/photo-1553279768-865429fa0078?w=500&q=80"),
            ("Organic Green Guava (2kg)", 350, "Fresh Fruits", "https://images.unsplash.com/photo-1536511110591-775b16f407b2?w=500&q=80"),
            ("Seasonal Lichi (100 pcs)", 800, "Fresh Fruits", "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80"),
            ("Fresh Sweet Pomegranate (1kg)", 450, "Fresh Fruits", "https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=500&q=80"),
            ("Organic Papaya (Large)", 150, "Fresh Fruits", "https://images.unsplash.com/photo-1526600329882-47c3f1405533?w=500&q=80"),
            ("Fresh Cavendish Banana (Dozen)", 120, "Fresh Fruits", "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=500&q=80"),

            # --- Organic Vegetables ---
            ("Fresh Red Spinach (Bundle)", 40, "Organic Vegetables", "https://images.unsplash.com/photo-1592419044706-39796d40f98c?w=500&q=80"),
            ("Organic Green Chili (250g)", 80, "Organic Vegetables", "https://images.unsplash.com/photo-1588253518679-1293149f132a?w=500&q=80"),
            ("Farm Fresh Tomato (1kg)", 120, "Organic Vegetables", "https://images.unsplash.com/photo-1518977676601-b53f02ac6d31?w=500&q=80"),
            ("Native Potato (Deshi) 5kg", 250, "Organic Vegetables", "https://images.unsplash.com/photo-1518977676601-b53f02ac6d31?w=500&q=80"),
            ("Fresh Cauliflower (Medium)", 60, "Organic Vegetables", "https://images.unsplash.com/photo-1568584711075-3d021a7c3fb3?w=500&q=80"),
            ("Organic Bitter Gourd (500g)", 50, "Organic Vegetables", "https://images.unsplash.com/photo-1583324113626-70df0f43aa2b?w=500&q=80"),

            # --- Books & Stationery ---
            ("Humayun Ahmed Collection Vol 1", 1200, "Books & Stationery", "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500&q=80"),
            ("Bengali Literature History", 850, "Books & Stationery", "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=500&q=80"),
            ("Advanced Programming in Python", 1500, "Books & Stationery", "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500&q=80"),
            ("Premium Leather Journal", 650, "Books & Stationery", "https://images.unsplash.com/photo-1544816155-12df9643f363?w=500&q=80"),
            ("Art Supplies Pro Kit", 2500, "Books & Stationery", "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=500&q=80"),
            ("Motivational Best Sellers Set", 1800, "Books & Stationery", "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500&q=80"),

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
        ]

        products = []
        for name, price, cat_name, img in products_data:
            cat = categories[cat_name]
            p, _ = Product.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': f"Premium {name} sourced directly from the finest producers and creators. Authenticity and quality are our top priorities.",
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
