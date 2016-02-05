from django.conf.urls import url
from django.contrib import admin

from judge_app.views \
    import ScoreSubmissionView, IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^score-submit/', ScoreSubmissionView.as_view(), name="score-submit"),
    url(r'^$', IndexView.as_view(), name="index"),
]
