from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import articles, authors, comments, news_letter, contact_us
from django.contrib.auth.models import auth, User
from django.contrib import auth
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import urllib.parse
# Create your views here.
def home(request):
	context = {}
	context['trending_news'] = articles.objects.filter(article_type="Trending News").latest('publish_date')
	context['gadgets'] = articles.objects.filter(article_type="Gadgets").latest('publish_date')
	context['technology'] = articles.objects.filter(article_type="Technology").latest('publish_date')
	context['all_articles']= articles.objects.order_by('-publish_date')[:10]
	context['pg_nation1'] = 1
	context['pg_nation2'] = 2
	context['pg_nation3'] = 3
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.filter(youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-article_page_views')[:3]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	pg_no = 1
	start_no = int(str(int(pg_no))+"0")
	end_no = int(str(pg_no+1) + "0")
	check_pg_nation= articles.objects.order_by('-publish_date')[start_no:end_no]
	if len(check_pg_nation) == 0:
		context['pg_nation2_check'] = False
		context['pg_nation3_check'] = False
		context['pg_nation_next'] = False
	else:
		context['pg_nation2_check'] = True
		check_pg_nation= articles.objects.order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation3_check'] = True
			context['pg_nation_next'] = True
	return render(request,"tech-index.html",context)
def more(request,pg_no):
	context = {}
	context['trending_news'] = articles.objects.filter(article_type="Trending News").latest('publish_date')
	context['gadgets'] = articles.objects.filter(article_type="Gadgets").latest('publish_date')
	context['technology'] = articles.objects.filter(article_type="Technology").latest('publish_date')
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.filter(youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-article_page_views')[:3]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	if int(pg_no) == 1:
		context['all_articles']= articles.objects.order_by('-publish_date')[:10]
		start_no = int(str(int(pg_no))+"0")
		end_no = int(str(pg_no+1) + "0")
		check_pg_nation= articles.objects.order_by('-publish_date')[start_no:end_no]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.order_by('-publish_date')[start_no+10:end_no+10]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True
	else:
		start_no = int(str(int(pg_no)-1)+"0")
		end_no = int(str(pg_no) + "0")
		context['all_articles']= articles.objects.order_by('-publish_date')[start_no:end_no]
		check_pg_nation= articles.objects.order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.order_by('-publish_date')[start_no+20:end_no+20]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True
	context['pg_nation1'] = int(pg_no)
	context['pg_nation2'] = int(pg_no) + 1
	context['pg_nation3'] = int(pg_no) + 2
	return render(request,"more_show.html",context)
def gadgets_(request):
	context = {}
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['gadget_article']= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[:10]
	context['trend_video'] = articles.objects.filter(article_type="Gadgets",youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.filter(article_type="Gadgets").order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-article_page_views')[:3]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	pg_no = 1
	start_no = int(str(int(pg_no))+"0")
	end_no = int(str(pg_no+1) + "0")
	check_pg_nation= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[start_no:end_no]
	if len(check_pg_nation) == 0:
		context['pg_nation2_check'] = False
		context['pg_nation3_check'] = False
		context['pg_nation_next'] = False
	else:
		context['pg_nation2_check'] = True
		check_pg_nation= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation3_check'] = True
			context['pg_nation_next'] = True
	context['pg_nation1'] = int(pg_no)
	context['pg_nation2'] = int(pg_no) + 1
	context['pg_nation3'] = int(pg_no) + 2
	return render(request,"tech-category-01.html",context)
def more_gadgets(request,pg_no):
	context = {}
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.filter(article_type="Gadgets",youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.filter(article_type="Gadgets").order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-article_page_views')[:3]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	if int(pg_no) == 1:
		context['gadget_article']= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[:10]
		start_no = int(str(int(pg_no))+"0")
		end_no = int(str(pg_no+1) + "0")
		check_pg_nation= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[start_no:end_no]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[start_no+10:end_no+10]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True
	else:
		start_no = int(str(int(pg_no)-1)+"0")
		end_no = int(str(pg_no) + "0")
		context['gadget_article']= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[start_no:end_no]
		check_pg_nation= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[start_no+20:end_no+20]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True

	context['pg_nation1'] = int(pg_no)
	context['pg_nation2'] = int(pg_no) + 1
	context['pg_nation3'] = int(pg_no) + 2
	return render(request,"more_gadget.html",context)

def videos_(request):
	context = {}
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.filter(youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-article_page_views')[:3]
	context['videos']= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[:10]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	pg_no = 1
	start_no = int(str(int(pg_no))+"0")
	end_no = int(str(pg_no+1) + "0")
	check_pg_nation= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no:end_no]
	if len(check_pg_nation) == 0:
		context['pg_nation2_check'] = False
		context['pg_nation3_check'] = False
		context['pg_nation_next'] = False
	else:
		context['pg_nation2_check'] = True
		check_pg_nation= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation3_check'] = True
			context['pg_nation_next'] = True
	context['pg_nation1'] = int(pg_no)
	context['pg_nation2'] = int(pg_no) + 1
	context['pg_nation3'] = int(pg_no) + 2
	return render(request,"tech-category-02.html",context)
def more_videos(request,pg_no):
	context = {}
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.filter(youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-article_page_views')[:3]
	context['videos']= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[:10]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	if int(pg_no) == 1:
		context['gadget_article']= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[:10]
		start_no = int(str(int(pg_no))+"0")
		end_no = int(str(pg_no+1) + "0")
		check_pg_nation= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no:end_no]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no+10:end_no+10]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True
	else:
		start_no = int(str(int(pg_no)-1)+"0")
		end_no = int(str(pg_no) + "0")
		context['gadget_article']= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no:end_no]
		check_pg_nation= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no+20:end_no+20]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True

	context['pg_nation1'] = int(pg_no)
	context['pg_nation2'] = int(pg_no) + 1
	context['pg_nation3'] = int(pg_no) + 2
	return render(request,"more_video.html",context)
def reviews_(request):
	context = {}
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.filter(youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[:3]
	context['reviews']= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[:10]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	pg_no = 1
	start_no = int(str(int(pg_no))+"0")
	end_no = int(str(pg_no+1) + "0")
	check_pg_nation= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no:end_no]
	if len(check_pg_nation) == 0:
		context['pg_nation2_check'] = False
		context['pg_nation3_check'] = False
		context['pg_nation_next'] = False
	else:
		context['pg_nation2_check'] = True
		check_pg_nation= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation3_check'] = True
			context['pg_nation_next'] = True
	context['pg_nation1'] = int(pg_no)
	context['pg_nation2'] = int(pg_no) + 1
	context['pg_nation3'] = int(pg_no) + 2
	return render(request,"tech-category-03.html",context)
def more_reviews(request,pg_no):
	context = {}
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.filter(youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[:3]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	if int(pg_no) == 1:
		context['reviews']= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[:10]
		start_no = int(str(int(pg_no))+"0")
		end_no = int(str(pg_no+1) + "0")
		check_pg_nation= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[start_no:end_no]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[start_no+10:end_no+10]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True
	else:
		start_no = int(str(int(pg_no)-1)+"0")
		end_no = int(str(pg_no) + "0")
		context['reviews']= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[start_no:end_no]
		check_pg_nation= articles.objects.filter(youtube_video_status=True).order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[start_no+20:end_no+20]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True

	context['pg_nation1'] = int(pg_no)
	context['pg_nation2'] = int(pg_no) + 1
	context['pg_nation3'] = int(pg_no) + 2
	return render(request,"more_review.html",context)
def contact_(request):
	context = {}
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['gadget_article']= articles.objects.filter(article_type="Gadgets").order_by('-publish_date')[:10]
	context['trend_video'] = articles.objects.filter(article_type="Gadgets",youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.filter(article_type="Gadgets").order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-article_page_views')[:3]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	if request.method == "POST":
		name=request.POST.get('name','')
		email=request.POST.get('email','')
		phone=request.POST.get('phone','')
		subject=request.POST.get('subject','')
		message=request.POST.get('message','')
		create=contact_us(name=name,email=email,phone=phone,subject=subject,message=message)
		create.save()
		messages.add_message(request,messages.SUCCESS,"Thanks for contacting us! we will get back to you shortely.")
		return redirect('tech-contact')
	return render(request,"tech-contact.html",context)

def articles_(request,article):
	article=urllib.parse.unquote(article)
	try:
		article_data=articles.objects.get(url_str=article)
	except articles.DoesNotExist:
		raise Http404("does not exist")
	context = {}
	context['article_data'] = article_data
	context['author_data'] = authors.objects.get(public_name=article_data.article_author)
	if request.user.is_authenticated and context['author_data'].public_name == article_data.article_author:
		context['author_data'].password="xxxxxxxxx"
	else:
		context['author_data'].username="xxxxxxxxx"
		context['author_data'].password="xxxxxxxxx"
	if article_data.id == 1:
		context['previous_article'] = articles.objects.last()
		if articles.objects.filter(id=int(article_data.id)+1).exists():
			context['next_article'] = articles.objects.get(id=int(article_data.id)+1)
	else:
		if articles.objects.filter(id=int(article_data.id)-1).exists():
			context['previous_article'] = articles.objects.get(id=int(article_data.id)-1)
		else:
		    for check_exist in range(int(article_data.id)-1,0,-1):
		        if articles.objects.filter(id=check_exist).exists():
		            context['previous_article']=articles.objects.get(id=int(check_exist))
		            break
		if articles.objects.filter(id=int(article_data.id)+1).exists():
			context['next_article'] = articles.objects.get(id=int(article_data.id)+1)
		else:
		    for check_exist_ in range(1,int(article_data.id)):
		        if articles.objects.filter(id=check_exist_).exists():
		            context['next_article']=articles.objects.get(id=check_exist_)
		            break
	if articles.objects.filter(article_type=article_data.article_type).exists():
		count=articles.objects.filter(article_type=article_data.article_type).count()
		counts = []
		for x in range(1,count):
			counts.append(x)
		if len(counts) >= 2:
			random_no1=random.choice(counts)
			counts.remove(random_no1)
			random_no2=random.choice(counts)
			context['recomended1'] = articles.objects.exclude(main_title=article_data.main_title).filter(article_type=article_data.article_type)[random_no1-1]
			context['recomended2'] = articles.objects.exclude(main_title=article_data.main_title).filter(article_type=article_data.article_type)[random_no2-1]
			context['recomended_exist'] = True
		else:
		    context['recomended_exist'] = False
	context['comment_status']=article_data.comment_status
	context['comments_show']=comments.objects.filter(post_title=article_data.main_title,post_id=article_data.id)
	context['comments_count']=comments.objects.filter(post_title=article_data.main_title,post_id=article_data.id).count()
	if request.method == "POST" and request.POST.get('reply','')=="start_reply":
		context['disply_reply'] = True
		context['email_val'] = request.POST.get('email_val','')
	else:
		context['disply_reply'] = False
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.exclude(main_title=article_data.main_title).filter(youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.exclude(main_title=article_data.main_title).order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.exclude(main_title=article_data.main_title).filter(article_type="Reviews").order_by('-article_page_views')[:3]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev) 
	article_data.article_page_views = int(article_data.article_page_views) + 1
	article_data.save()
	return render(request,"tech-single.html",context)
def author_(request,author_name):
	author_name=author_name.split("-")
	author_name=" ".join(author_name)
	context = {}
	try:
		context['author_data']= authors.objects.get(public_name=author_name)
		context['author_data'].username = "xxxxxxxxx"
		context['author_data'].password = "xxxxxxxxx"
	except authors.DoesNotExist:
		raise Http404("does not exist")
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.filter(youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[:3]
	context['author_post']= articles.objects.filter(article_author=author_name).order_by('-publish_date')[:10]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	pg_no = 1
	start_no = int(str(int(pg_no))+"0")
	end_no = int(str(pg_no+1) + "0")
	check_pg_nation= articles.objects.filter(article_author=author_name).order_by('-publish_date')[start_no:end_no]
	if len(check_pg_nation) == 0:
		context['pg_nation2_check'] = False
		context['pg_nation3_check'] = False
		context['pg_nation_next'] = False
	else:
		context['pg_nation2_check'] = True
		check_pg_nation= articles.objects.filter(article_author=author_name).order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation3_check'] = True
			context['pg_nation_next'] = True
	context['pg_nation1'] = int(pg_no)
	context['pg_nation2'] = int(pg_no) + 1
	context['pg_nation3'] = int(pg_no) + 2
	return render(request,"tech-author.html",context)
def more_author(request,author_name,pg_no):
	author_name=author_name.split("-")
	author_name=" ".join(author_name)
	context = {}
	try:
		context['author_data']= authors.objects.get(public_name=author_name)
		context['author_data'].username = "xxxxxxxxx"
		context['author_data'].password = "xxxxxxxxx"
	except authors.DoesNotExist:
		raise Http404("does not exist")
	context['nav_article1']= articles.objects.filter(article_type="Science").order_by('-publish_date')[:4]
	context['nav_article2']= articles.objects.filter(article_type="Technology").order_by('-publish_date')[:4]
	context['nav_article3']= articles.objects.filter(article_type="Entertainment").order_by('-publish_date')[:4]
	context['nav_article6']= articles.objects.filter(article_type="Sports").order_by('-publish_date')[:4]
	context['nav_article4']= articles.objects.filter(article_type="AutoMobile").order_by('-publish_date')[:4]
	context['nav_article5']= articles.objects.filter(article_type="Worldwide").order_by('-publish_date')[:4]
	context['nav_article7']= articles.objects.filter(article_type="Health Care").order_by('-publish_date')[:4]
	context['nav_article8']= articles.objects.filter(article_type="Others").order_by('-publish_date')[:4]
	context['trend_video'] = articles.objects.filter(youtube_video_status=True).order_by('-article_page_views')[:3]
	context['popular_post']= articles.objects.order_by('-article_page_views')[:3]
	context['recent_reviews']= articles.objects.filter(article_type="Reviews").order_by('-publish_date')[:3]
	for star in context['recent_reviews']:
		star_rev = star.review_star
		star.review_star = range(star_rev)
	if int(pg_no) == 1:
		context['author_post']= articles.objects.filter(article_author=author_name).order_by('-publish_date')[:10]
		start_no = int(str(int(pg_no))+"0")
		end_no = int(str(pg_no+1) + "0")
		check_pg_nation= articles.objects.filter(article_author=author_name).order_by('-publish_date')[start_no:end_no]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.filter(article_author=author_name).order_by('-publish_date')[start_no+10:end_no+10]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True
	else:
		start_no = int(str(int(pg_no)-1)+"0")
		end_no = int(str(pg_no) + "0")
		context['author_post']= articles.objects.filter(article_author=author_name).order_by('-publish_date')[start_no:end_no]
		check_pg_nation= articles.objects.filter(article_author=author_name).order_by('-publish_date')[start_no+10:end_no+10]
		if len(check_pg_nation) == 0:
			context['pg_nation2_check'] = False
			context['pg_nation3_check'] = False
			context['pg_nation_next'] = False
		else:
			context['pg_nation2_check'] = True
			check_pg_nation= articles.objects.filter(article_author=author_name).order_by('-publish_date')[start_no+20:end_no+20]
			if len(check_pg_nation) == 0:
				context['pg_nation3_check'] = False
				context['pg_nation_next'] = False
			else:
				context['pg_nation3_check'] = True
				context['pg_nation_next'] = True

	context['pg_nation1'] = int(pg_no)
	context['pg_nation2'] = int(pg_no) + 1
	context['pg_nation3'] = int(pg_no) + 2
	return render(request,"more_author.html",context)
def redirect_me(request,redirect_link):
	if authors.objects.filter(linkedin_link=redirect_link).exists():
		confirm_redirect = "https://www.linkedin.com/in/"+redirect_link
		return HttpResponseRedirect(confirm_redirect)
	elif authors.objects.filter(facebook_link=redirect_link).exists():
		confirm_redirect = "https://facebook.com/"+redirect_link
		return HttpResponseRedirect(confirm_redirect)
	elif authors.objects.filter(instagram_link=redirect_link).exists():
		confirm_redirect = "https://instagram.com/"+redirect_link
		return HttpResponseRedirect(confirm_redirect)
	elif authors.objects.filter(pintrest_link=redirect_link).exists():
		confirm_redirect = "https://www.pinterest.com//"+redirect_link
		return HttpResponseRedirect(confirm_redirect)
	elif authors.objects.filter(website_link=redirect_link).exists():
		confirm_redirect = "http://"+redirect_link
		return HttpResponseRedirect(confirm_redirect)
	elif authors.objects.filter(youtube_link=redirect_link).exists():
		confirm_redirect = "https://youtube.com/"+redirect_link
		return HttpResponseRedirect(confirm_redirect)
	else:
		raise Http404("does not exist")

def add_reply(request):
	if request.method =="POST" and request.POST.get('confirm_reply','') == "confirmed_" and comments.objects.filter(post_title=request.POST.get('post_title',''),post_id=request.POST.get('post_number','')).exists():
		author_reply = request.POST.get('comment_reply','')
		post_title=request.POST.get('post_title','')
		post_id=request.POST.get('post_number','')
		post_url=request.POST.get('post_url','')
		email_public=request.POST.get('email_public','')
		add_author_comment=comments.objects.get(post_title=post_title,post_id=post_id,email=email_public)
		add_author_comment.comment_reply=author_reply
		add_author_comment.save()
		return redirect('tech-single',article=post_url)
	return redirect('home')
def add_comment(request):
	if request.method=="POST" and request.POST.get('create_comment') == "confirm_create":
		post_title=request.POST.get('post_title')
		post_id=request.POST.get('post_number','')
		post_url=request.POST.get('post_url','')
		name=request.POST.get('public_name','')
		email=request.POST.get('public_email','')
		comment=request.POST.get('public_comment','')
		comment_image="images/thumb_WXpnKM0.png"
		if comments.objects.filter(email=email,post_title=post_title,post_id=post_id).exists():
			messages.add_message(request,messages.WARNING,"You have alreday commented on this article!")
			return redirect('tech-single',article=post_url)
		website_link=request.POST.get('public_website','')
		create=comments(post_title=post_title,post_id=post_id,name=name,email=email,comment=comment,comment_image=comment_image,website_link=website_link)
		create.save()
		messages.add_message(request,messages.SUCCESS,"Thank you for your comment!!")
		return redirect('tech-single',article=post_url)
	else:
		return redirect('home')
def add_newsletter(request):
	if request.method == "POST":
		email=request.POST.get('email_newsletter','')
		post_url=request.POST.get('post_url','')
		if news_letter.objects.filter(email=email).exists():
			messages.add_message(request,messages.WARNING,"You have alreday subscribed to our newsletter!")
			return redirect('home')
		else:
			create=news_letter(email=email)
			create.save()
			messages.add_message(request,messages.SUCCESS,"You have susscribed to our newsletter!")
			return redirect('home')
	else:
		return redirect('home')
def privacy(request):
    return render(request,"privacy.html")