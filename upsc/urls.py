



from django.contrib import admin
#from django.urls import path, include

#urlpatterns = [
 #   path('admin/', admin.site.urls),
 #   path('', include('mains_practice.urls')),  # ✅ connects your app's urls
#]


from django.urls import path, include

urlpatterns = [
    path('', include('mains_practice.urls')),
]
