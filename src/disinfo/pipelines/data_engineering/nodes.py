import re
from typing import Any, Dict

import pandas as pd
import unicodeblock.blocks

text_col = 12 #list(data.columns).index('tweet_text')
user_display_name = 2

def remove_rt(data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    og = data.loc[data['is_retweet'] == False]
    rt = data.loc[data['is_retweet']]
    return dict(
        og=og,
        rt=rt
    )

def remove_empty(data: pd.DataFrame) -> Dict[str, list]:
    content = []
    empty = []
    rows = data.values.tolist()
    #text_col = list(data.columns).index('tweet_text')
    for row in rows:
        clean_tweet = re.match('(.*?)http.*?\s?(.*?)', row[text_col])
        if clean_tweet is None:
            text = row[text_col]
        else:
            text = clean_tweet.group(1) + clean_tweet.group(2)
        text.strip()
        if len(text) == 0:
            empty.append(row)
        else:
            row[text_col] = text
            content.append(row)

    print('cont ' + str(len(content)))
    print('empt ' + str(len(empty)))

    return dict(
        content=content,
        empty=empty
    )

def language_split(rows: list) -> Dict[str, list]:
    arabic = []
    latin = []
    cyrillic = []
    kanji = []
    korean = []
    other = []

    everyone_has_it = [
        'ARROWS',
        'BASIC_PUNCTUATION',
        'BLOCK_ELEMENTS',
        'BOX_DRAWING',
        'BRAILLE_PATTERNS',
        'COMBINING_MARKS_FOR_SYMBOLS',
        'CURRENCY_SYMBOLS',
        'DIGIT',
        'DINGBATS',
        'DOMINO_TILES',
        'EMOTICONS',
        'ENCLOSED_ALPHANUMERIC_SUPPLEMENT',
        'ENCLOSED_ALPHANUMERICS',
        'FULLWIDTH_DIGIT',
        'GENERAL_PUNCTUATION',
        'GEOMETRIC_SHAPES',
        'LETTERLIKE_SYMBOLS',
        'MAHJONG_TILES',
        'MATHEMATICAL_ALPHANUMERIC_SYMBOLS',
        'MATHEMATICAL_OPERATORS',
        'MISCELLANEOUS_MATHEMATICAL_SYMBOLS_A',
        'MISCELLANEOUS_SYMBOLS',
        'MISCELLANEOUS_SYMBOLS_AND_ARROWS',
        'MISCELLANEOUS_SYMBOLS_AND_PICTOGRAPHS',
        'MISCELLANEOUS_TECHNICAL',
        'MUSICAL_SYMBOLS',
        'NUMBER_FORMS',
        'OPTICAL_CHARACTER_RECOGNITION',
        'PLAYING_CARDS',
        'PRIVATE_USE_AREA',
        'SMALL_FORM_VARIANTS',
        'SPACE',
        'SPACING_MODIFIER_LETTERS',
        'SPECIALS',
        'SUPERSCRIPTS_AND_SUBSCRIPTS',
        'SUPPLEMENTAL_ARROWS_A',
        'SUPPLEMENTAL_ARROWS_B',
        'SUPPLEMENTAL_MATHEMATICAL_OPERATORS',
        'SUPPLEMENTAL_PUNCTUATION',
        'SUPPLEMENTARY_PRIVATE_USE_AREA_A',
        'SUPPLEMENTARY_PRIVATE_USE_AREA_B',
        'TAGS',
        'TRANSPORT_AND_MAP_SYMBOLS',
        'VARIATION_SELECTORS',
        None,
    ]

    langOpts = {
        'ru': [
            'CYRILLIC',
            'CYRILLIC_EXTENDED_A',
            'CYRILLIC_EXTENDED_B',
            'CYRILLIC_EXTENDED_C',
            'CYRILLIC_SUPPLEMENTARY',
        ],
        'ko': [
            'HANGUL_COMPATIBILITY_JAMO',
            'HANGUL_JAMO',
            'HANGUL_SYLLABLES',
        ],
        'ja': [
            'CJK_COMPATIBILITY',
            'CJK_COMPATIBILITY_FORMS',
            'CJK_SYMBOLS_AND_PUNCTUATION',
            'CJK_UNIFIED_IDEOGRAPHS',
            'CJK_UNIFIED_IDEOGRAPHS_EXTENSION_A',
            'ENCLOSED_CJK_LETTERS_AND_MONTHS',
            'ENCLOSED_IDEOGRAPHIC_SUPPLEMENT',
            'HIRAGANA',
            'KATAKANA',
        ],
        'ar_fa': [
            'ARABIC',
            'ARABIC_PRESENTATION_FORMS_A',
            'ARABIC_PRESENTATION_FORMS_B',
            'ARABIC_SUPPLEMENT',
        ],
        'en_tr': [
            'BASIC_LATIN',
            'FULLWIDTH_LATIN',
            'LATIN_1_SUPPLEMENT',
            'LATIN_EXTENDED_A',
            'LATIN_EXTENDED_B',
            'LATIN_EXTENDED_C',
            'LATIN_EXTENDED_D',
            'LATIN_EXTENDED_ADDITIONAL',
            'LATIN_EXTENDED_LETTER',
        ]
    }
    langSort = list(langOpts.keys())
    knownLetters = {}

    for row in rows:
        words = row[text_col].replace('\n', ' ').replace('  ', ' ').split(' ')
        #twitter_lang = tweet[headers.index('tweet_language')]
        my_langs = []

        langCount = {}

        for word in words:
            if ('@' in word) or ('https//' in word) or ('http//' in word):
                continue
            hashtag = (len(word) > 0 and word[0] == "#")
            for letter in word:
                if letter in ['.', u'\u00ad']:
                    continue
                try:
                    block = knownLetters[letter]
                except:
                    block = unicodeblock.blocks.of(letter)
                    knownLetters[letter] = block

                for language in langSort:
                    if block in langOpts[language]:
                        if hashtag and language == 'en_tr':
                            break
                        if language not in my_langs:
                            my_langs.append(language)
                            langCount[language] = 1
                        else:
                            langCount[language] += 1
                        break

        my_langs = sorted(my_langs, reverse=True, key=lambda lang: langCount[lang])
        # if twitter_lang == "ar" and len(my_langs) > 0 and my_langs[0] == "en_tr":
        #     print(langCount)

        if len(my_langs) == 0:
            other.append(row)
        elif my_langs[0] == "ar_fa":
            arabic.append(row)
        elif my_langs[0] == "en_tr":
            latin.append(row)
        elif my_langs[0] == "ru":
            cyrillic.append(row)
        elif my_langs[0] == "ja":
            kanji.append(row)
        elif my_langs[0] == "ko":
            korean.append(row)
        else:
            other.append(row)

    print('arfa ' + str(len(arabic)))
    print('entr ' + str(len(latin)))
    print('ru ' + str(len(cyrillic)))
    print('ja ' + str(len(kanji)))
    print('ko ' + str(len(korean)))
    print('ot ' + str(len(other)))

    return dict(
        ar_fa=arabic,
        en_tr=latin,
        ru_ot=cyrillic,
        ja_zh=kanji,
        ko=korean,
        other=other
    )

def arabic_split(rows: list) -> Dict[str, list]:
    ar = []
    fa = []
    ur = []

    urdu = 'ٹ ڈ ڑ ں ے ھ'
    persian = 'پچژگ'

    for row in rows:
        text = row[text_col]
        found_urdu = False
        found_persian = False
        for letter in urdu:
            if letter in text:
                ur.append(row)
                found_urdu = True
                break
        if not found_urdu:
            for letter in persian:
                if letter in text:
                    fa.append(row)
                    found_persian = True
                    break
        if (not found_urdu) and (not found_persian):
            ar.append(row)

    # print('ar ' + str(len(ar)))
    # print('fa ' + str(len(fa)))
    # print('ur ' + str(len(ur)))

    return dict(
        ar=ar,
        fa=fa,
        ur=ur
    )

def latin_split(rows: list) -> Dict[str, list]:
    en = []
    tr = []
    turkish = 'ÇŞĞİÖÜşği̇ı'
    for row in rows:
        text = row[text_col] # + "_" + row[user_display_name]
        found_turkish = False
        for letter in turkish:
            if letter in text:
                tr.append(row)
                found_turkish = True
                break
        if not found_turkish:
            en.append(row)

    # print('en ' + str(len(en)))
    # print('tr ' + str(len(tr)))
    return dict(
        en=en,
        tr=tr
    )


def split_data(data: pd.DataFrame, example_test_data_ratio: float) -> Dict[str, Any]:
    # data.columns = [
    #     "sepal_length",
    #     "sepal_width",
    #     "petal_length",
    #     "petal_width",
    #     "target",
    # ]
    #print(len(data))
    classes = sorted(data["tweet_language"].unique())
    # One-hot encoding for the target variable
    data = pd.get_dummies(data, columns=["tweet_language"], prefix="", prefix_sep="")

    # Shuffle all the data
    data = data.sample(frac=1).reset_index(drop=True)

    # Split to training and testing data
    n = data.shape[0]
    n_test = int(n * example_test_data_ratio)
    training_data = data.iloc[n_test:, :].reset_index(drop=True)
    test_data = data.iloc[:n_test, :].reset_index(drop=True)

    # Split the data to features and labels
    train_data_x = training_data.loc[:, "tweet_text":"tweet_client_name"]
    train_data_y = training_data[classes]
    test_data_x = test_data.loc[:, "tweet_text":"tweet_client_name"]
    test_data_y = test_data[classes]

    # When returning many variables, it is a good practice to give them names:
    return dict(
        train_x=train_data_x,
        train_y=train_data_y,
        test_x=test_data_x,
        test_y=test_data_y,
    )
