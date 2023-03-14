from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
   'Fi': ''
}

@register.filter()
def currency(value, code='rub'):

   postfix = CURRENCIES_SYMBOLS[code]
   return f'{value} {postfix}'

@register.filter()
def censor(value):
   bad_words = ('скотина', 'бляха')

   if not isinstance(value, str):
      raise TypeError(f"unresolved type '{type(value)}' expected  type 'str'")

   for word in value.split():
      if word.lower() in bad_words:
         value = value.replace(word, f"{word[0]}{'*' * (len(word) - 2)}{word[-1]}")
   return value