"""
Management command to populate the database with sample data
Run with: python manage.py populate_sample_data
"""
from django.core.management.base import BaseCommand
from api.models import Category, Material, Product, Testimonial


class Command(BaseCommand):
    help = 'Populate database with sample data for PrintBox3D'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create Categories
        categories_data = [
            {
                'name': 'Home Decor',
                'description': 'Unique decorative pieces for your living space'
            },
            {
                'name': 'Gadgets & Accessories',
                'description': 'Functional prints for everyday use'
            },
            {
                'name': 'Custom Orders',
                'description': 'Bring your ideas to life with bespoke prints'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            self.stdout.write(f'  {"Created" if created else "Found"} category: {category.name}')

        # Create Materials
        materials_data = [
            {
                'name': 'PLA',
                'description': 'Standard biodegradable 3D printing material',
                'properties': 'Easy to print, biodegradable, low warping'
            },
            {
                'name': 'ABS',
                'description': 'Durable engineering plastic',
                'properties': 'Strong, impact resistant, heat resistant'
            },
            {
                'name': 'PETG',
                'description': 'Strong and flexible material',
                'properties': 'Food safe, chemical resistant, durable'
            },
            {
                'name': 'TPU',
                'description': 'Flexible rubber-like material',
                'properties': 'Flexible, elastic, impact resistant'
            }
        ]

        materials = {}
        for mat_data in materials_data:
            material, created = Material.objects.get_or_create(
                name=mat_data['name'],
                defaults={
                    'description': mat_data['description'],
                    'properties': mat_data['properties']
                }
            )
            materials[mat_data['name']] = material
            self.stdout.write(f'  {"Created" if created else "Found"} material: {material.name}')

        # Create Products
        products_data = [
            {
                'name': 'Geometric Planter',
                'description': 'A modern geometric planter perfect for succulents and small plants. Made with premium PLA material for durability and aesthetic appeal.',
                'price': 899,
                'category': 'Home Decor',
                'material': 'PLA',
                'color': 'White',
                'dimensions': '12cm x 12cm x 10cm',
                'weight': 150,
                'stock_quantity': 10,
                'is_featured': True
            },
            {
                'name': 'Phone Stand Pro',
                'description': 'Ergonomic phone stand designed for optimal viewing angles. Sturdy ABS construction ensures stability for all phone sizes.',
                'price': 599,
                'category': 'Gadgets & Accessories',
                'material': 'ABS',
                'color': 'Black',
                'dimensions': '8cm x 7cm x 10cm',
                'weight': 80,
                'stock_quantity': 15,
                'is_featured': True
            },
            {
                'name': 'Modern Wall Art',
                'description': 'Contemporary geometric wall art piece that adds a modern touch to any space. Lightweight and easy to mount.',
                'price': 1299,
                'category': 'Home Decor',
                'material': 'PLA',
                'color': 'Multiple',
                'dimensions': '30cm x 30cm x 2cm',
                'weight': 200,
                'stock_quantity': 8,
                'is_featured': True
            },
            {
                'name': 'Cable Organizer Set',
                'description': 'Keep your desk tidy with this practical cable management solution. Set includes multiple organizers.',
                'price': 449,
                'category': 'Gadgets & Accessories',
                'material': 'PLA',
                'color': 'Black',
                'dimensions': '5cm x 3cm x 2cm (each)',
                'weight': 30,
                'stock_quantity': 25,
                'is_featured': False
            },
            {
                'name': 'Desk Organizer',
                'description': 'Multi-compartment desk organizer to keep your workspace neat and productive.',
                'price': 799,
                'category': 'Gadgets & Accessories',
                'material': 'ABS',
                'color': 'Gray',
                'dimensions': '20cm x 15cm x 8cm',
                'weight': 180,
                'stock_quantity': 12,
                'is_featured': False
            },
            {
                'name': 'Decorative Vase',
                'description': 'Elegant twisted vase design perfect for artificial or dried flowers.',
                'price': 1099,
                'category': 'Home Decor',
                'material': 'PLA',
                'color': 'White',
                'dimensions': '15cm x 15cm x 25cm',
                'weight': 220,
                'stock_quantity': 6,
                'is_featured': True
            },
            {
                'name': 'Laptop Stand',
                'description': 'Ergonomic laptop stand that improves posture and cooling. Adjustable height.',
                'price': 1499,
                'category': 'Gadgets & Accessories',
                'material': 'ABS',
                'color': 'Black',
                'dimensions': '25cm x 20cm x 15cm',
                'weight': 300,
                'stock_quantity': 10,
                'is_featured': True
            },
            {
                'name': 'Wall Shelf',
                'description': 'Minimalist floating wall shelf for books, plants, or decorative items.',
                'price': 1799,
                'category': 'Home Decor',
                'material': 'PETG',
                'color': 'Wood Tone',
                'dimensions': '40cm x 15cm x 5cm',
                'weight': 400,
                'stock_quantity': 5,
                'is_featured': False
            },
            {
                'name': 'Headphone Stand',
                'description': 'Stylish headphone stand that keeps your desk organized and headphones safe.',
                'price': 699,
                'category': 'Gadgets & Accessories',
                'material': 'PLA',
                'color': 'Black',
                'dimensions': '12cm x 12cm x 25cm',
                'weight': 120,
                'stock_quantity': 18,
                'is_featured': True
            }
        ]

        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'category': categories[prod_data['category']],
                    'material': materials[prod_data['material']],
                    'color': prod_data['color'],
                    'dimensions': prod_data['dimensions'],
                    'weight': prod_data['weight'],
                    'stock_quantity': prod_data['stock_quantity'],
                    'is_available': True,
                    'is_featured': prod_data['is_featured']
                }
            )
            self.stdout.write(f'  {"Created" if created else "Found"} product: {product.name}')

        # Create Testimonials
        testimonials_data = [
            {
                'name': 'Rajesh Kumar',
                'company': 'Tech Innovations',
                'rating': 5,
                'message': 'PrintBox3D delivered exceptional quality prototypes for our product launch. The attention to detail and fast turnaround exceeded our expectations!',
                'is_featured': True
            },
            {
                'name': 'Priya Sharma',
                'company': '',
                'rating': 5,
                'message': 'I ordered a custom wedding gift and it turned out perfect! The team was helpful throughout the process. Highly recommended!',
                'is_featured': True
            },
            {
                'name': 'Amit Patel',
                'company': 'Design Studio Pro',
                'rating': 4,
                'message': 'Great service and quality prints. Used them for multiple architectural models. Very satisfied with the results.',
                'is_featured': True
            }
        ]

        for test_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=test_data['name'],
                defaults={
                    'company': test_data['company'],
                    'rating': test_data['rating'],
                    'message': test_data['message'],
                    'is_featured': test_data['is_featured']
                }
            )
            self.stdout.write(f'  {"Created" if created else "Found"} testimonial: {testimonial.name}')

        self.stdout.write(self.style.SUCCESS('\nSample data created successfully!'))
        self.stdout.write('\nSummary:')
        self.stdout.write(f'  Categories: {Category.objects.count()}')
        self.stdout.write(f'  Materials: {Material.objects.count()}')
        self.stdout.write(f'  Products: {Product.objects.count()}')
        self.stdout.write(f'  Testimonials: {Testimonial.objects.count()}')
