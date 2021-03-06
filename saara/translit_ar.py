import sys, os, glob, json, codecs, platform

import arabic.ArabicTransliterator
from arabic.ArabicTransliterator import ALA_LC_Transliterator
import mishkal.tashkeel.tashkeel as tashkeel

class TranslitArabic(object):
    def __init__(self):
        self.transliterator = ALA_LC_Transliterator()

    def transliterate(self, text, vocalize=True):
        """
        >>> ar_translit.transliterate(text, vocalize=True)
        :param text:
        :param vocalize:
        :return:
        """
        voc = text
        if vocalize:
            vocalizer = tashkeel.TashkeelClass()
            voc = vocalizer.tashkeel(text)
        return self.transliterator.do(voc.strip())

    def transliterate_df(self, inputdf):
        import pandas as pd
        outputdf = pd.DataFrame(columns=['transliterations'])
        for i, row in inputdf.iterrows():
            for elem in row:
                t = self.transliterate(elem.strip(), vocalize=True)
                t_df = pd.DataFrame({'transliterations': [t]}, index=[i])
                outputdf = outputdf.append(t_df)
        return outputdf

    def tests(self):
        """
        $ python -m saara.translit_ar tests
        :return:
        """
        import pandas as pd
        import saara.utils as sagas

        inputfile1 = 'data/phrases.csv'
        inputfile2 = 'data/nouns.csv'

        inputdf = pd.read_csv(inputfile1)
        outputdf = self.transliterate_df(inputdf)
        d = pd.concat([inputdf, outputdf], axis=1)
        sagas.print_df(d)

    def translit(self, trac_unk, text):
        """
        t: ‫من فضلك، هناك عند الزاوية على اليسار.‬
        $ python -m saara.translit_ar translit True t

        :param text:
        :return:
        """
        # from sagas.nlu.common import get_from_clip
        # if text is None:
        #     text = get_from_clip()

        r=self.transliterate(text)
        r=r.replace('[UNK]','').strip() if trac_unk else r
        print(text)
        print(r)

    def fixtures(self):
        """
        $ python -m saara.translit_ar fixtures
        :return:
        """
        sents=['من فضلك، هناك عند الزاوية على اليسار.‬',
               ]
        for s in sents:
            self.translit(True, s)

ar_translit=TranslitArabic()

if __name__ == '__main__':
    import fire
    fire.Fire(TranslitArabic)

