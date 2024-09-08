'''

path('', Index.as_view(), name='index'): Asosiy sahifani ko'rsatadi.

path('shop/', Products.as_view(), name='shop'): Mahsulotlar ro'yxatini ko'rsatadigan savdo sahifasini ochadi.

path('cat-pr/<int:pk>/', category_product, name='cat-pr'): Berilgan kategoriya bo'yicha mahsulotlarni ko'rsatadi.

path('detail/<int:pk>/', DetailProduct.as_view(), name='detail'): Mahsulotning batafsil ma'lumotlari sahifasini ochadi.

path('rate/<int:product_id>/<int:rating>/', rate): Foydalanuvchiga mahsulotga reyting qo'yish imkoniyatini beradi.

path('login/', user_login, name='login'): Foydalanuvchini tizimga kirish sahifasiga yo'naltiradi.

path('logout/', user_logout, name='logout'): Foydalanuvchini tizimdan chiqaradi.

path('register/', user_register, name='register'): Yangi foydalanuvchini ro'yxatdan o'tkazish sahifasiga yo'naltiradi.

path('add-comment/<int:pk>/', create_comment, name='comment'): Mahsulotga izoh qo'shish uchun sahifaga yo'naltiradi.

path('comment/<int:pk>/', view_comment, name='view_comment'): Mahsulotga qo'shilgan izohlarni ko'rsatadi.

path('cart/', cart, name='cart'): Foydalanuvchining savatini ko'rsatadi.

path('to-cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'): Savatga mahsulot qo'shis

h yoki olib tashlashni boshqaradi.

path('clear-cart/', clear_cart, name='clear_cart'): Savatni tozalash funksiyasini amalga oshiradi.

path('payment/', create_checkout_sessions, name='payment'): To'lov jarayonini boshlaydi.

path('success/', success_payment, name='success'): Muvaffaqiyatli to'lovdan so'ng tasdiqlash sahifasini ko'rsatadi.

'''