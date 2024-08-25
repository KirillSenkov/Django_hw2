from django import forms
from django.contrib import admin, messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Article, Tag, Scope


class ScopeInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        main_tags_cnt = sum(1 for form in self.forms
                            if form.cleaned_data.get('is_main', False))

        if main_tags_cnt == 0:
            raise ValidationError('Необходимо установить основной тэг для статьи.')
        elif main_tags_cnt > 1:
            raise ValidationError('Основным может быть только один тэг.')

    def save_new(self, form, commit=True):

        try:
            return super().save_new(form, commit=commit)
        except IntegrityError:
            form._non_form_errors = self.error_class(['Для статьи '
                'может быть установлен только один основной тэг.'])
            raise ValueError('Для статьи может быть установлен'
                             ' только один основной тэг.')

    def save_existing(self, form, instance, commit=True):
        try:
            return super().save_existing(form, instance, commit=commit)
        except IntegrityError:
            form._non_form_errors = self.error_class(['Для статьи может быть'
                                    ' установлен только один основной тэг.'])
            raise ValueError('Для статьи может быть установлен'
                             ' только один основной тэг.')

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormSet
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except IntegrityError:
            self.message_user(request, 'Ошибка: для одной статьи может быть'
                ' установлен только один основной тэг.', level=messages.ERROR)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
