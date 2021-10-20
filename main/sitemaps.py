from django.contrib.sitemaps import Sitemap
from .models import articles
from django.urls import reverse

class articlesSitemap(Sitemap):
	def items(self):
		return articles.objects.all()
class StaticViewSitemap(Sitemap):
	def items(self):
		return['tech-contact']
	def location(self, item):
		return reverse(item)
