from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    
    # Debug-Toolbar erscheint am linken Bildschirmrand
    path('__debug_toolbar__', include('debug_toolbar.urls')),
    
    # Paypal-Page einbinden
    path('paypal/', include('paypal.standard.ipn.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# für Fehlermeldungen URL hier definieren 
# -> bezieht sich auf die views.py
# -> anderer Bezugsort ist möglich
handler404 ='shop.views.fehler404'
