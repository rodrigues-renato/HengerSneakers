# Henger Sneakers - Quick Start Guide

## 🚀 Getting Started with Your New Sneakers E-commerce

Follow these steps to get your Henger Sneakers platform up and running.

---

## Step 1: Install Dependencies

```bash
# Make sure you're in the project directory
cd /home/renato/Documents/HENGER/pizzaria

# Activate your virtual environment (if not already active)
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# Install requirements (includes new Pillow dependency)
pip install -r requirements.txt
```

---

## Step 2: Apply Database Migrations

```bash
# Create migration files (if needed)
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# You should see migrations being applied for:
# - menu.0002_produto_sneakers_update
# - pedidos.0007_remove_pedido_status_alter_pedido_metodo_pagamento
```

---

## Step 3: Create Admin User (if not exists)

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

---

## Step 4: Generate Demo Sneaker Products

```bash
# This will create 40 sample sneaker products
python utils/create_products.py
```

**Sample output:**
```
Creating sneakers...
✓ Nike Air Max - Tam. 42
✓ Adidas Ultraboost - Tam. 40
✓ Puma Suede Classic - Tam. 38
... (40 products created)
```

---

## Step 5: (Optional) Create Demo Users and Orders

```bash
# Create sample users
python utils/create_users.py

# Create sample orders (requires users and products)
python utils/create_orders.py
```

---

## Step 6: Run the Development Server

```bash
python manage.py runserver
```

Server should start at: **http://127.0.0.1:8000**

---

## 🎯 Access Points

### Customer Interface
- **Home/Products**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/clientes/logar/
- **Register**: http://127.0.0.1:8000/clientes/registrar/
- **Cart**: http://127.0.0.1:8000/pedidos/carrinho/
- **Checkout**: http://127.0.0.1:8000/pedidos/finalizar/
- **Order History**: http://127.0.0.1:8000/pedidos/historico/

### Admin Interface
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Dashboard**: http://127.0.0.1:8000/dashboard/

---

## 🛍️ Test the Shopping Flow

1. **Browse Products**
   - Go to homepage
   - See sneakers with brand, size, color, price
   - Filter by category (Masculino, Feminino, Unissex, Infantil)

2. **Add to Cart**
   - Click "Add to Cart" on products
   - View cart to see items

3. **Checkout**
   - Click "Finalizar Pedido"
   - Select/add delivery address
   - Choose payment method (Credit Card, Debit Card, Pix, or Boleto)
   - Complete order

4. **View Order History**
   - Go to "Meus Pedidos"
   - See past orders with details

---

## 📊 Admin Tasks

### Managing Products

```bash
# Access admin panel
http://127.0.0.1:8000/admin/

# Navigate to: Menu > Produtos
# You can:
# - Add new sneakers
# - Edit existing products
# - Update stock levels
# - Upload product images
# - Filter by brand, category, size
# - Search by name, brand, color
```

### Product Fields
- **Nome**: Model name (e.g., "Air Max 90")
- **Marca**: Brand (e.g., "Nike")
- **Preço**: Price in BRL
- **Descrição**: Product description
- **Categoria**: Masculino/Feminino/Unissex/Infantil
- **Cor**: Color
- **Tamanho**: Size (35-45)
- **Estoque**: Stock quantity
- **Imagem**: Product image (upload JPG/PNG)

---

## 🔧 Troubleshooting

### Migration Issues

**Problem**: Old pizza data conflicts with new sneaker fields

**Solution**:
```bash
# Option 1: Clear product table and re-populate
python manage.py shell

>>> from menu.models import Produto
>>> Produto.objects.all().delete()
>>> exit()

python utils/create_products.py
```

**Option 2**: Manually update products via admin panel

### Image Upload Issues

**Problem**: Images not showing up

**Solution**:
```bash
# Ensure media directory exists
mkdir -p media/sneakers

# Check settings.py has:
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# In urls.py (development only):
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Payment Method Not Showing

**Problem**: Old payment options still appearing

**Solution**: Clear browser cache or use incognito mode

---

## 📝 Next Steps

1. **Customize Templates**
   - Update branding (logo, colors)
   - See `TEMPLATE_UPDATES.md` for recommendations

2. **Add Real Products**
   - Remove demo products
   - Add your actual sneaker inventory
   - Upload product photos

3. **Configure Payment Gateway**
   - Integrate with payment provider (Stripe, PagSeguro, etc.)
   - Update payment processing logic

4. **Deploy to Production**
   - Set DEBUG=False
   - Configure production database (PostgreSQL)
   - Set up proper static/media file serving
   - Add domain and SSL

---

## 🎨 Customization Tips

### Update Branding
```python
# pizzaria/settings.py
# Change references from "pizzaria" to your preferred name

# templates/base.html
# Update <title> and logo
```

### Adjust Product Categories
```python
# menu/models.py
# Modify categoria choices if needed
categoria = models.CharField(
    max_length=50, 
    choices=[
        ("Running", "Running"),
        ("Basketball", "Basketball"),
        ("Casual", "Casual"),
        ("Skateboarding", "Skateboarding")
    ]
)
```

---

## 📞 Support

If you encounter issues:
1. Check `MIGRATION_SUMMARY.md` for what changed
2. Review `TEMPLATE_UPDATES.md` for template modifications
3. Verify migrations are applied: `python manage.py showmigrations`
4. Check Django logs for errors

---

**Happy selling! 👟✨**
