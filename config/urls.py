from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from chat import views
from Social_Network import app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_network.urls')),
    path('', include('Social_Network.routes')),
    path('inbox/', app.inbox, name='inbox'),
    path(
    	'chat/<int:conversation_id>/',
    	views.room, 
    	name='chat_room'
    ),
    path(
    	"chat/start/<int:user_id>/",
    	views.start_chat,
    	name="start_chat"
	)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)