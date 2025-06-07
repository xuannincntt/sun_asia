from modeltranslation.translator import translator, TranslationOptions
from .models import Project

class ProjectTranslationOptions(TranslationOptions):
    fields = ('name', 'product', 'investor')

translator.register(Project, ProjectTranslationOptions)
