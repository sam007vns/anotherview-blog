from django.contrib import admin
from .models import *
from django.contrib.sitemaps import ping_google
from youtube_transcript_api import YouTubeTranscriptApi

@admin.register(articles)
class articlesAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyinject.js',)
    def save_model(self, request, obj, form, change):
    	author_name=authors.objects.get(username=request.user.username).public_name
    	obj.article_author = author_name
    	author_url=author_name.split(" ")
    	author_url="-".join(author_url)
    	obj.author_url=author_url
    	main_title=obj.main_title
    	url_str=main_title.split(" ")
    	url_str="-".join(url_str)
    	obj.url_str=url_str
    	if obj.youtube_video_status:
            youtube_url=obj.youtube_video_url
            tube_count=youtube_url.count("=")
            if tube_count == 1:
                youtube_url=youtube_url.split("=")[1]
                obj.youtube_embed=youtube_url
            elif tube_count == 2:
                youtube_url=youtube_url.split("=")[1]
                youtube_url=youtube_url.split('&f')[0]
                obj.youtube_embed=youtube_url
            elif tube_count == 0:
                youtube_url=youtube_url.split(".be/")[1]
                obj.youtube_embed=youtube_url
    	super().save_model(request, obj, form, change)
    	try:
    	    ping_google()
    	except Exception:
    	    pass

class generate_contantAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        youtube_gen_link=obj.youtube_link_togenerate
        check_count=youtube_gen_link.count("=")
        if check_count == 1:
            youtube_url_af=youtube_gen_link.split("=")[1]
            obj.youtube_link_togenerate=youtube_url_af
        elif check_count == 2:
            youtube_url_af=youtube_gen_link.split("=")[1]
            obj.youtube_link_togenerate=youtube_url_af.split('&f')[0]
        elif check_count == 0:
            youtube_url_af=youtube_gen_link.split(".be/")[1]
            obj.youtube_link_togenerate=youtube_url_af
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(obj.youtube_link_togenerate)
            if obj.translate:
                translated=False
                for transcript in transcript_list:
                    if transcript.is_translatable:
                        for langu in  transcript.translation_languages:
                            if langu['language_code'] == "hi":
                                content_from_vid=transcript.translate('hi').fetch()
                                translated=True
                                break
                        if translated:
                            break
                        else:
                            if transcript.language_code == "en" or transcript.language_code == "en-IN":
                                content_from_vid=transcript.fetch()
                                break
                    else:
                        if transcript.language_code == "en" or transcript.language_code == "en-IN":
                            content_from_vid=transcript.fetch()
                            break
            else:
                for transcript in transcript_list:
                    if transcript.language_code == "en" or transcript.language_code == "en-IN":
                        content_from_vid=transcript.fetch()
                        break
            # content_from_vid=YouTubeTranscriptApi.get_transcript(obj.youtube_link_togenerate)
            final_content = " "
            for x in content_from_vid:
                final_content += x['text']
                final_content += " "
            final_content = final_content.replace('\n'," ")
            obj.generated_content=final_content
            obj.username=request.user.username
            super().save_model(request, obj, form, change)
        except Exception:
            obj.username=request.user.username
            obj.generated_content="No transcript found in the video or it is disabled kindly delete this entry!"
            super().save_model(request, obj, form, change)
admin.site.register(generate_contant,generate_contantAdmin)
admin.site.register(authors)
# admin.site.register(articles, articlesAdmin)
admin.site.register(comments)
admin.site.register(news_letter)
admin.site.register(contact_us)
# Register your models here.
