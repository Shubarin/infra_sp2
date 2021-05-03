from django.contrib import admin

from .models.categories import Category
from .models.comments import Comments
from .models.genres import Genre
from .models.users import MyUser
from .models.review import Review
from .models.titles import Title

admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Genre)
admin.site.register(MyUser)
admin.site.register(Review)
admin.site.register(Title)
