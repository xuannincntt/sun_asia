from modeltranslation.translator import translator, TranslationOptions
from .models import NewsCategory, News

class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(NewsCategory, NewsCategoryTranslationOptions)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
    
translator.register(News, NewsTranslationOptions)
