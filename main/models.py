from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.urls import reverse

class authors(models.Model):
	username = models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	public_name = models.CharField(max_length=30)
	account_access = models.BooleanField(default = True)
	email = models.CharField(max_length=30)
	phone = models.IntegerField(blank=True)
	password = models.CharField(max_length=30,blank=True)
	about = models.TextField()
	instagram_link=models.TextField(blank=True)
	facebook_link=models.TextField(blank=True)
	linkedin_link=models.TextField(blank=True)
	youtube_link=models.TextField(blank=True)
	pintrest_link=models.TextField(blank=True)
	twitter_link=models.TextField(blank=True)
	website_link=models.TextField(blank=True)
	image_upload_permission = models.BooleanField(default = False)
	video_upload_permission = models.BooleanField(default = False)
	author_image = models.ImageField(upload_to='images/')
	last_login=models.DateTimeField(default=timezone.datetime.now())
	instagram_available=models.BooleanField(default=False)
	facebook_available=models.BooleanField(default=False)
	linkedin_available=models.BooleanField(default=False)
	youtube_available=models.BooleanField(default=False)
	pintrest_available=models.BooleanField(default=False)
	twitter_available=models.BooleanField(default=False)
	website_available=models.BooleanField(default=False)
	author_url= models.TextField()

	def __str__(self):
		return self.username

class articles(models.Model):
	main_title = models.CharField(max_length=300,verbose_name="Main Title")
	ARTICLE_TYPES = [
        ('Trending News', 'Trending News'),
        ('Science', 'Science'),
        ('Technology', 'Technology'),
        ('Entertainment', 'Entertainment'),
        ('Sports', 'Sports'),
        ('Automobile', 'Automobile'),
        ('Worldwide', 'Worldwide'),
        ('Reviews', 'Reviews'),
        ('Health Care', 'Health Care'),
        ('Gadgets', 'Gadgets'),
        ('Others', 'Others'),
    ]
	publish_date = models.DateTimeField(default=timezone.datetime.now())
	article_type = models.CharField(max_length=30,choices=ARTICLE_TYPES,verbose_name="Categories")
	article_author = models.CharField(max_length=30, editable=False)
	main_image = models.ImageField(upload_to='images/',verbose_name="Top Image")
	main_img_caption = models.TextField(verbose_name="Title Discription")
	second_title = models.TextField(verbose_name="Body")
	second_title_text_para1 = models.TextField(verbose_name="Title 2 Paragraph 1",blank=True,editable=True)
	second_title_text_para2 = models.TextField(verbose_name="Title 2 Paragraph 2",blank=True,editable=True)
	second_image = models.ImageField(upload_to='images/',blank=True,verbose_name="Second Image(optional)")
	third_title=models.TextField(verbose_name="Title 3",blank=True,editable=True)
	third_title_text_para1 = models.TextField(verbose_name="Title 3 Paragraph 1",blank=True,editable=True)
	third_title_text_para2 = models.TextField(verbose_name="Title 3 Paragraph 2",blank=True,editable=True)
	third_title_text_para3 = models.TextField(verbose_name="Title 3 Paragraph 3",blank=True,editable=True)
	third_title_text_para4 = models.TextField(verbose_name="Title 3 Paragraph 4",blank=True,editable=True)
	third_image = models.ImageField(upload_to='images/',blank=True,verbose_name="Third Image(optional)")
	third_title_text_key_point1 = models.TextField(verbose_name="Key-Point1(optional)",blank=True,editable=True)
	third_title_text_key_point2 = models.TextField(verbose_name="Key-Point2(optional)",blank=True,editable=True)
	third_title_text_key_point3 = models.TextField(verbose_name="Key-Point3(optional)",blank=True,editable=True)
	third_title_text_key_point4 = models.TextField(verbose_name="Key-Point4(optional)",blank=True,editable=True)
	third_title_text_key_point5 = models.TextField(verbose_name="Key-Point5(optional)",blank=True,editable=True)
	fourth_title = models.TextField(blank=True,verbose_name="Title 4(optional)",editable=True)
	fourth_title_text_para1 = models.TextField(blank=True,verbose_name="Title 4 Paragraph 1(optional)",editable=True)
	fourth_title_text_para2 = models.TextField(blank=True,verbose_name="Title 4 Paragraph 2(optional)",editable=True)
	fourth_title_text_para3 = models.TextField(blank=True,verbose_name="Title 4 Paragraph 3(optional)",editable=True)
	article_tag1 = models.CharField(max_length=50,verbose_name="Article Tag 1")
	article_tag2 = models.CharField(max_length=50,verbose_name="Article Tag 2")
	article_tag3 = models.CharField(max_length=50,verbose_name="Article Tag 3")
	article_tag4 = models.CharField(max_length=50,verbose_name="Article Tag 4")
	fourth_image = models.ImageField(upload_to='images/',blank=True,verbose_name="Fourth Image(optional)")
	article_display = models.BooleanField(default = True,verbose_name="Show on Website")
	article_page_views=models.IntegerField(default = 0, editable=False)
	video_clip = models.FileField(upload_to='video/',blank=True,editable=False)
	url_str = models.TextField(editable=False)
	comment_status=models.BooleanField(default = True,verbose_name="Allow Comments")
	youtube_video_status=models.BooleanField(default = False,verbose_name="Include Youtube Video")
	youtube_video_url = models.TextField(blank=True,verbose_name="Youtube Video Link(optional)")
	youtube_embed = models.TextField(blank=True,editable=False)
	review_star = models.IntegerField(blank=True,default=1,verbose_name="Star Rating(Max- 5)")
	author_url= models.CharField(max_length=30, editable=False)
	def __str__(self):
		return self.main_title
	def get_absolute_url(self):
	    return reverse('tech-single',args=[str(self.url_str)])
class comments(models.Model):
	name = models.CharField(max_length=30)
	email = models.CharField(max_length=100)
	website_link=models.CharField(max_length=100,blank=True)
	comment=models.TextField()
	post_title=models.CharField(max_length=300)
	post_id=models.IntegerField()
	comment_reply=models.TextField(blank=True)
	comment_date = models.DateTimeField(default=timezone.datetime.now())
	comment_image = models.ImageField(upload_to='images/',blank=True)
	def __str__(self):
		return self.comment

class news_letter(models.Model):
	email = models.CharField(max_length=100)
	def __str__(self):
		return self.email

class contact_us(models.Model):
	name=models.CharField(max_length=30)
	email=models.TextField()
	phone=models.CharField(max_length=12)
	subject=models.TextField()
	message=models.TextField()
	message_date=models.DateTimeField(default=timezone.datetime.now())
	def __str__(self):
		return self.email

class generate_contant(models.Model):
    username=models.CharField(max_length=30,editable=False)
    youtube_link_togenerate=models.TextField()
    generated_content=models.TextField(blank=True)
    translate=models.BooleanField(verbose_name="Translate to Hindi(if possible)")
    def __str__(self):
        return self.username
