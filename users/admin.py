from django.contrib import admin
from users.models import UserProfile,WelcomeModel
from club.models import Club,ClubMember,ClubFollower
from news.models import News
from events.models import Event

class ClubsAdmin(admin.ModelAdmin):
    list_display=('name','tagline','created_date','modified_date')

class ClubMembersAdmin(admin.ModelAdmin):
    list_display=('club','app_user','is_admin')

class ClubFollowersAdmin(admin.ModelAdmin):
    list_display=('club','app_user','modified_date')

class NewsAdmin(admin.ModelAdmin):
    list_dispaly=('club','user','created_date')
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Club,ClubsAdmin)
admin.site.register(ClubMember,ClubMembersAdmin)
admin.site.register(ClubFollower,ClubFollowersAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Event)
admin.site.register(WelcomeModel)