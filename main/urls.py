from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
path("",views.home,name="home"),
path("more/<int:pg_no>",views.more,name="more"),
path("gadgets",views.gadgets_,name="tech-category-01"),
path("videos",views.videos_,name="tech-category-02"),
path("contact",views.contact_,name="tech-contact"),
path("reviews",views.reviews_,name="tech-category-03"),
path("articles/<str:article>",views.articles_,name="tech-single"),
path("author/<str:author_name>",views.author_,name="tech-author"),
path("author/<str:author_name>/<int:pg_no>",views.more_author,name="more_author"),
path("redirect/<str:redirect_link>",views.redirect_me,name="redirect_me"),
path("add_reply/",views.add_reply,name="add_reply"),
path("add_comment/",views.add_comment,name="add_comment"),
path("add_newsletter/",views.add_newsletter,name="add_newsletter"),
path("gadgets/more/<int:pg_no>",views.more_gadgets,name="more_gadgets"),
path("videos/more/<int:pg_no>",views.more_videos,name="more_videos"),
path("reviews/more/<int:pg_no>",views.more_reviews,name="more_reviews"),
path("privacy-policy/",views.privacy,name="privacy"),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)