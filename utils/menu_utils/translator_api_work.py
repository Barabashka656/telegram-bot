from googletrans import Translator 
from googletrans.constants import LANGCODES, LANGUAGES

translator = Translator()
print(translator.translate(text='я егорка урод гниль гнида сука мразь обоссышь чмо негр', src='ru', dest='mk').text)
print(translator.detect('жыпка.').lang)
print(translator.detect('This sentence is written in English.').confidence)


