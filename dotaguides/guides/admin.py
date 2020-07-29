from django.contrib import admin
from .models import Guide, Hero

admin.site.register(Guide)
admin.site.register(Hero)

class GuideAdmin(admin.ModelAdmin):
    fields= ('title','slug','text','category','published')
    def save_model(self, request, obj, form, change): 
        instance = form.save(commit=False)
        if not hasattr(instance,'author'):
            instance.author = request.user
        instance.author = request.user
        instance.save()
        form.save_m2m()
        return instance

    def save_formset(self, request, form, formset, change): 

        def set_user(instance):
            if not instance.author:
                instance.author = request.user
            instance.author = request.user
            instance.save()

        if formset.model == Guide:
            instances = formset.save(commit=False)
            map(set_user, instances)
            formset.save_m2m()
            return instances
        else:
            return formset.save()