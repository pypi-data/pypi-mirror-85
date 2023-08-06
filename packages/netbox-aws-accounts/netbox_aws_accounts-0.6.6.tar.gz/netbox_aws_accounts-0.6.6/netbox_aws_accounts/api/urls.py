from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('accounts', AccountsViewSet)
router.register('regions', RegionsViewSet)

urlpatterns = router.urls