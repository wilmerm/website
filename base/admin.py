from django.contrib import admin

from base.models import (Setting, AdvancedSetting, SocialNetwork, Slide, 
Schedule, Brand, Question)




admin.site.register(Setting)
admin.site.register(AdvancedSetting)
admin.site.register(SocialNetwork)
admin.site.register(Slide)
admin.site.register(Schedule)
admin.site.register(Brand)
admin.site.register(Question)