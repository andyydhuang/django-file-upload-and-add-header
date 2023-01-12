from django.urls import path
from .views import deleteSingleDocument
from .views import deleteDocuments
from .views import (
    DocListView,
    DocDeleteView,
    HandleDocDeleteView,
    DocUploadView,
    HandleDocUploadView,
)

urlpatterns = [
    path('deleteDoc/<int:doc_id>/', deleteSingleDocument),
    path('deleteDocs/', deleteDocuments),
    path('', DocListView.as_view(), name='my-view'),
    path('file-upload', DocUploadView.as_view(), name='file-upload'),
    path('handelUpload', HandleDocUploadView.as_view(), name='my-handle-upload'),
    path('delete', DocDeleteView.as_view(), name='my-delete'),
    path('handelDelete', HandleDocDeleteView.as_view(), name='my-handle-delete'),
]

