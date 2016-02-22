from django.conf.urls import url
from django.contrib import admin

from judge_app.views import (
    ScoreSubmissionView,
    IndexView,
    AwardsList,
    AwardsDetail,
    PresentationList,
    WinnersPDFView,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^score-submit/$', ScoreSubmissionView.as_view(), name="score-submit"),
    url(r'^results/list/$', AwardsList.as_view(), name="awards-list"),
    url(r'^results/presentation/$', PresentationList.as_view(), name="presentation-list"),
    url(r'^results/as_pdf/$', WinnersPDFView.as_view(), name="winners-pdf"),
    url(r'^result/detail/(?P<slug>[\w\+%_&\-\\\/]+)/$',
        AwardsDetail.as_view(), name="result-detail"),
    url(r'^$', IndexView.as_view(), name="index"),
]
