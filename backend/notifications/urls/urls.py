from django.urls import path, include

urlpatterns = [
    path('api/', include('notifications.urls')),  # Подключаем маршруты из приложения "notifications"
]
