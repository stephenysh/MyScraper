import googletrans
from googletrans import Translator

print(googletrans.LANGUAGES)

translator = Translator()
text="داء المرتفعات، والمعروف أيضا باسم مرض الجبال الحاد ، hypobaropathy، أو soroche، هو التأثير المرضي للعلو الشاهق على البشر، والناجم عن التعرض الحاد للضغط الجزئى المنخفض للأكسجين على علو شاهق. ويحدث ذلك عادة فوق 2400 متر (8000 قدما)."
result = translator.translate(text)
print(result.text)