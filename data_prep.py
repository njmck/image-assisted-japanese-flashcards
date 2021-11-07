# !/usr/bin/env python3
# @AUTHOR : njmck

import xmltodict
import json



# "JMdict_e.gz" downloaded from http://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project
# xml extracted from "JMdict_e.gz" and filename changed "JMdict_e" -> "JMdict_e.xml"
xml_filename = "JMdict_e.xml"

# The original XML file has issues with some data being imported properly into dictionaries.
# So, we can remove some unnecessary characters like '&' and ';'.
# Specify tags to clean by removing '&' and ';':
tags_to_clean = ["pos", "misc", "field", "s_inf"]
# Replace the target string
for tag in tags_to_clean:
	tidy_data = tidy_data.replace('<' + tag + '>&', '<' + tag + '>')
	tidy_data = tidy_data.replace(';</' + tag + '>', '</' + tag + '>')

# Write the file out again with a new file name:
xml_filename_clean = xml_filename[:-4] + '_tidy.xml'
with open(xml_filename_clean, 'w') as file:
	file.write(tidy_data)

# Opens the WWWJDIC dictionary xml file and returns an Ordered Dictionary.
# Useful JMDict info: http://nihongo.monash.edu/wwwjdicinf.html#code_tag
with open(xml_filename_clean, "r+") as xml_file:
	xml_str = xml_file.read()
	xml_import = xmltodict.parse(xml_str)
word_list = [_ for _ in xml_import['JMdict']['entry']]

## ---- Export/Import filterted XML data using JSON files ---- ##

# Export "xml_import" to json file:
# Export json file:
import json

json_filename = "JMDict_xml_import.json"
json_xml_import = json.dumps(xml_import)
with open(json_filename, 'w') as jsonfile:
    json.dump(json_xml_import, jsonfile)

# Re-import json file of imported XML as OrderedDict:
import json
import collections

json_filename = "xml_import.json"
with open(json_filename, 'r') as jsonfile:
    json_load = json.load(jsonfile)
word_list = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(json_load)

## ---- Sort JMDict data into a dictionary with desired formatting ---- ##

# Sorting each data type (kanji, kana, definition, misc, etc.) with an individual loop below
# is easier to write and is simpler to maintain, if a bit slower.

filtered_dict = {"main_list": [],
                 "kana_list": [],
                 "en_list": [],
                 "pos_main_list": [],
                 "misc_main_list": [],
                 "field_main_list": [],
                 "s_inf_main_list": [],
                 "en_list_neat": []
                 }

# Generate a kanji list containing kanji if it exists, otherwise use kana:
for entry in word_list:
    child_list = []
    if 'k_ele' in entry:
        if isinstance(entry['k_ele'], dict):
            child_list.append(entry['k_ele']['keb'])
        else:
            for k_ele in entry['k_ele']:
                child_list.append(k_ele['keb'])
    if isinstance(entry['r_ele'], dict):
        child_list.append(entry['r_ele']['reb'])
    else:
        for r_ele in entry['r_ele']:
            child_list.append(r_ele['reb'])
    filtered_dict['main_list'].append(child_list)

# Generate a kana list:
for entry in word_list:
    child_list = []
    if isinstance(entry['r_ele'], dict):
        child_list.append(entry['r_ele']['reb'])
    else:
        for r_ele in entry['r_ele']:
            child_list.append(r_ele['reb'])
    filtered_dict['kana_list'].append(child_list)

# Generate a dictionary for tags for easier data filtering.
# Keep this tag dictionary updated with each new version of JMdict:
tag_dict = {"bra": "Brazilian",
            "hob": "Hokkaido-ben",
            "ksb": "Kansai-ben",
            "ktb": "Kantou-ben",
            "kyb": "Kyoto-ben",
            "kyu": "Kyuushuu-ben",
            "nab": "Nagano-ben",
            "osb": "Osaka-ben",
            "rkb": "Ryuukyuu-ben",
            "thb": "Touhoku-ben",
            "tsb": "Tosa-ben",
            "tsug": "Tsugaru-ben",
            "agric": "agriculture",
            "anat": "anatomy",
            "archeol": "archeology",
            "archit": "architecture",
            "art": "art, aesthetics",
            "astron": "astronomy",
            "audvid": "audiovisual",
            "aviat": "aviation",
            "baseb": "baseball",
            "biochem": "biochemistry",
            "biol": "biology",
            "bot": "botany",
            "Buddh": "Buddhism",
            "bus": "business",
            "chem": "chemistry",
            "Christn": "Christianity",
            "cloth": "clothing",
            "comp": "computing",
            "cryst": "crystallography",
            "ecol": "ecology",
            "econ": "economics",
            "elec": "electricity, elec. eng.",
            "electr": "electronics",
            "embryo": "embryology",
            "engr": "engineering",
            "ent": "entomology",
            "finc": "finance",
            "fish": "fishing",
            "food": "food, cooking",
            "gardn": "gardening, horticulture",
            "genet": "genetics",
            "geogr": "geography",
            "geol": "geology",
            "geom": "geometry",
            "go": "go (game)",
            "golf": "golf",
            "gramm": "grammar",
            "grmyth": "Greek mythology",
            "hanaf": "hanafuda",
            "horse": "horse racing",
            "law": "law",
            "ling": "linguistics",
            "logic": "logic",
            "MA": "martial arts",
            "mahj": "mahjong",
            "math": "mathematics",
            "mech": "mechanical engineering",
            "med": "medicine",
            "met": "meteorology",
            "mil": "military",
            "music": "music",
            "ornith": "ornithology",
            "paleo": "paleontology",
            "pathol": "pathology",
            "pharm": "pharmacy",
            "phil": "philosophy",
            "photo": "photography",
            "physics": "physics",
            "physiol": "physiology",
            "print": "printing",
            "psy": "psychiatry",
            "psych": "psychology",
            "rail": "railway",
            "Shinto": "Shinto",
            "shogi": "shogi",
            "sports": "sports",
            "stat": "statistics",
            "sumo": "sumo",
            "telec": "telecommunications",
            "tradem": "trademark",
            "vidg": "video games",
            "zool": "zoology",
            "ateji": "ateji (phonetic) reading",
            "ik": "word containing irregular kana usage",
            "iK": "word containing irregular kanji usage",
            "io": "irregular okurigana usage",
            "oK": "word containing out-dated kanji or kanji usage",
            "rK": "rarely-used kanji form",
            "abbr": "abbreviation",
            "arch": "archaism",
            "char": "character",
            "chn": "children's language",
            "col": "colloquialism",
            "company": "company name",
            "creat": "creature",
            "dated": "dated term",
            "dei": "deity",
            "derog": "derogatory",
            "doc": "document",
            "ev": "event",
            "fam": "familiar language",
            "fem": "female term or language",
            "fict": "fiction",
            "form": "formal or literary term",
            "given": "given name or forename, gender not specified",
            "group": "group",
            "hist": "historical term",
            "hon": "honorific or respectful (sonkeigo) language",
            "hum": "humble (kenjougo) language",
            "id": "idiomatic expression",
            "joc": "jocular, humorous term",
            "leg": "legend",
            "m-sl": "manga slang",
            "male": "male term or language",
            "myth": "mythology",
            "net-sl": "Internet slang",
            "obj": "object",
            "obs": "obsolete term",
            "obsc": "obscure term",
            "on-mim": "onomatopoeic or mimetic word",
            "organization": "organization name",
            "oth": "other",
            "person": "full name of a particular person",
            "place": "place name",
            "poet": "poetical term",
            "pol": "polite (teineigo) language",
            "product": "product name",
            "proverb": "proverb",
            "quote": "quotation",
            "rare": "rare",
            "relig": "religion",
            "sens": "sensitive",
            "serv": "service",
            "sl": "slang",
            "station": "railway station",
            "surname": "family or surname",
            "uk": "word usually written using kana alone",
            "unclass": "unclassified name",
            "vulg": "vulgar expression or word",
            "work": "work of art, literature, music, etc. name",
            "X": "rude or X-rated term (not displayed in educational software)",
            "yoji": "yojijukugo",
            "adj-f": "noun or verb acting prenominally",
            "adj-i": "adjective (keiyoushi)",
            "adj-ix": "adjective (keiyoushi) - yoi/ii class",
            "adj-kari": "'kari' adjective (archaic)",
            "adj-ku": "'ku' adjective (archaic)",
            "adj-na": "adjectival nouns or quasi-adjectives (keiyodoshi)",
            "adj-nari": "archaic/formal form of na-adjective",
            "adj-no": "nouns which may take the genitive case particle 'no'",
            "adj-pn": "pre-noun adjectival (rentaishi)",
            "adj-shiku": "'shiku' adjective (archaic)",
            "adj-t": "'taru' adjective",
            "adv": "adverb (fukushi)",
            "adv-to": "adverb taking the 'to' particle",
            "aux": "auxiliary",
            "aux-adj": "auxiliary adjective",
            "aux-v": "auxiliary verb",
            "conj": "conjunction",
            "cop": "copula",
            "ctr": "counter",
            "exp": "expressions (phrases, clauses, etc.)",
            "int": "interjection (kandoushi)",
            "n": "noun (common) (futsuumeishi)",
            "n-adv": "adverbial noun (fukushitekimeishi)",
            "n-pr": "proper noun",
            "n-pref": "noun, used as a prefix",
            "n-suf": "noun, used as a suffix",
            "n-t": "noun (temporal) (jisoumeishi)",
            "num": "numeric",
            "pn": "pronoun",
            "pref": "prefix",
            "prt": "particle",
            "suf": "suffix",
            "unc": "unclassified",
            "v-unspec": "verb unspecified",
            "v1": "Ichidan verb",
            "v1-s": "Ichidan verb - kureru special class",
            "v2a-s": "Nidan verb with 'u' ending (archaic)",
            "v2b-k": "Nidan verb (upper class) with 'bu' ending (archaic)",
            "v2b-s": "Nidan verb (lower class) with 'bu' ending (archaic)",
            "v2d-k": "Nidan verb (upper class) with 'dzu' ending (archaic)",
            "v2d-s": "Nidan verb (lower class) with 'dzu' ending (archaic)",
            "v2g-k": "Nidan verb (upper class) with 'gu' ending (archaic)",
            "v2g-s": "Nidan verb (lower class) with 'gu' ending (archaic)",
            "v2h-k": "Nidan verb (upper class) with 'hu/fu' ending (archaic)",
            "v2h-s": "Nidan verb (lower class) with 'hu/fu' ending (archaic)",
            "v2k-k": "Nidan verb (upper class) with 'ku' ending (archaic)",
            "v2k-s": "Nidan verb (lower class) with 'ku' ending (archaic)",
            "v2m-k": "Nidan verb (upper class) with 'mu' ending (archaic)",
            "v2m-s": "Nidan verb (lower class) with 'mu' ending (archaic)",
            "v2n-s": "Nidan verb (lower class) with 'nu' ending (archaic)",
            "v2r-k": "Nidan verb (upper class) with 'ru' ending (archaic)",
            "v2r-s": "Nidan verb (lower class) with 'ru' ending (archaic)",
            "v2s-s": "Nidan verb (lower class) with 'su' ending (archaic)",
            "v2t-k": "Nidan verb (upper class) with 'tsu' ending (archaic)",
            "v2t-s": "Nidan verb (lower class) with 'tsu' ending (archaic)",
            "v2w-s": "Nidan verb (lower class) with 'u' ending and 'we' conjugation (archaic)",
            "v2y-k": "Nidan verb (upper class) with 'yu' ending (archaic)",
            "v2y-s": "Nidan verb (lower class) with 'yu' ending (archaic)",
            "v2z-s": "Nidan verb (lower class) with 'zu' ending (archaic)",
            "v4b": "Yodan verb with 'bu' ending (archaic)",
            "v4g": "Yodan verb with 'gu' ending (archaic)",
            "v4h": "Yodan verb with 'hu/fu' ending (archaic)",
            "v4k": "Yodan verb with 'ku' ending (archaic)",
            "v4m": "Yodan verb with 'mu' ending (archaic)",
            "v4n": "Yodan verb with 'nu' ending (archaic)",
            "v4r": "Yodan verb with 'ru' ending (archaic)",
            "v4s": "Yodan verb with 'su' ending (archaic)",
            "v4t": "Yodan verb with 'tsu' ending (archaic)",
            "v5aru": "Godan verb - -aru special class",
            "v5b": "Godan verb with 'bu' ending",
            "v5g": "Godan verb with 'gu' ending",
            "v5k": "Godan verb with 'ku' ending",
            "v5k-s": "Godan verb - Iku/Yuku special class",
            "v5m": "Godan verb with 'mu' ending",
            "v5n": "Godan verb with 'nu' ending",
            "v5r": "Godan verb with 'ru' ending",
            "v5r-i": "Godan verb with 'ru' ending (irregular verb)",
            "v5s": "Godan verb with 'su' ending",
            "v5t": "Godan verb with 'tsu' ending",
            "v5u": "Godan verb with 'u' ending",
            "v5u-s": "Godan verb with 'u' ending (special class)",
            "v5uru": "Godan verb - Uru old class verb (old form of Eru)",
            "vi": "intransitive verb",
            "vk": "Kuru verb - special class",
            "vn": "irregular nu verb",
            "vr": "irregular ru verb, plain form ends with -ri",
            "vs": "noun or participle which takes the aux. verb suru",
            "vs-c": "su verb - precursor to the modern suru",
            "vs-i": "suru verb - included",
            "vs-s": "suru verb - special class",
            "vt": "transitive verb",
            "vz": "Ichidan verb - zuru verb (alternative form of -jiru verbs)",
            "gikun": "gikun (meaning as reading) or jukujikun (special kanji reading)",
            "ik": "word containing irregular kana usage",
            "ok": "out-dated or obsolete kana usage",
            "uK": "word usually written using kanji alone"
            }

# Generate simplified nested lists for English definitions:
for entry in word_list:
    if isinstance(entry['sense'], list):
        gloss_list = []
        for sense in entry['sense']:
            if '#text' in sense['gloss']:
                text_list = [sense['gloss']['#text']]
            else:
                text_list = []
                for gloss in sense['gloss']:
                    text_list.append(gloss['#text'])
            gloss_list.append(text_list)
    else:
        gloss_list = []
        if '#text' in entry['sense']['gloss']:
            text_list  = [entry['sense']['gloss']['#text']]
            gloss_list.append(text_list)
        else:
            text_list = []
            for gloss in entry['sense']['gloss']:
                text_list.append(gloss['#text'])
            gloss_list.append(text_list)
    filtered_dict['en_list'].append(gloss_list)

# 'pos' key denotes the word type (noun, adjective, etc.):
for entry in word_list:
    if isinstance(entry['sense'], list):
        pos_parent_list = []
        for sense in entry['sense']:
            if 'pos' in sense:
                if isinstance(sense['pos'], list):
                    pos_list = sense['pos']
                else:
                    pos_list = [sense['pos']]
            pos_parent_list.append(pos_list)
    else:
        pos_parent_list = []
        if 'pos' in entry['sense']:
            if isinstance(entry['sense']['pos'], list):
                pos_list = entry['sense']['pos']
            else:
                pos_list = [entry['sense']['pos']]
        pos_parent_list.append(pos_list)
    filtered_dict['pos_main_list'].append(pos_parent_list)

# 'misc' denotes miscellaneous information about the word (usually kana, colloquialism, etc.):
for entry in word_list:
    if isinstance(entry['sense'], list):
        misc_parent_list = []
        for sense in entry['sense']:
            if 'misc' in sense:
                if isinstance(sense['misc'], list):
                    misc_list = sense['misc']
                else:
                    misc_list = [sense['misc']]
            else:
                misc_list = []
            misc_parent_list.append(misc_list)
    else:
        misc_parent_list = []
        if 'misc' in entry['sense']:
            if isinstance(entry['sense']['misc'], list):
                misc_list = entry['sense']['misc']
            else:
                misc_list = [entry['sense']['misc']]
        else:
            misc_list = []
        misc_parent_list.append(misc_list)
    filtered_dict['misc_main_list'].append(misc_parent_list)

# 'field' denotes whether the word belongs to a particular field of expertise (science, sports, etc.):
for entry in word_list:
    if isinstance(entry['sense'], list):
        field_parent_list = []
        for sense in entry['sense']:
            if 'field' in sense:
                if isinstance(sense['field'], list):
                    field_list = sense['field']
                else:
                    field_list = [sense['field']]
            else:
                field_list = []
            field_parent_list.append(field_list)
    else:
        field_parent_list = []
        if 'field' in entry['sense']:
            if isinstance(entry['sense']['field'], list):
                field_list = entry['sense']['field']
            else:
                field_list = [entry['sense']['field']]
        else:
            field_list = []
        field_parent_list.append(field_list)
    filtered_dict['field_main_list'].append(field_parent_list)

# s_inf denotes additional miscellaneous information specific for each definition:
for entry in word_list:
    if isinstance(entry['sense'], list):
        s_inf_parent_list = []
        for sense in entry['sense']:
            if 's_inf' in sense:
                if isinstance(sense['s_inf'], list):
                    s_inf_list = sense['s_inf']
                else:
                    s_inf_list = [sense['s_inf']]
            else:
                s_inf_list = []
            s_inf_parent_list.append(s_inf_list)
    else:
        s_inf_parent_list = []
        if 's_inf' in entry['sense']:
            if isinstance(entry['sense']['s_inf'], list):
                s_inf_list = entry['sense']['s_inf']
            else:
                s_inf_list = [entry['sense']['s_inf']]
        else:
            s_inf_list = []
        s_inf_parent_list.append(s_inf_list)
    filtered_dict['s_inf_main_list'].append(s_inf_parent_list)

# Make the final formatted strings:
for i_0 in range(len(en_list)):
    # 'pos'
    gloss_num = 1
    gloss_main_list = []
    for i_1 in range(len(en_list[i_0])):
        unabbr_pos_list = [tag_dict[i_2] for i_2 in pos_main_list[i_0][i_1]]
        if i_1 > 0:
            if pos_main_list[i_0][i_1] != pos_main_list[i_0][i_1 - 1]:
                pos_str = '<b>' + ', '.join(unabbr_pos_list) + ':|' + '</b>'
            else:
                pos_str = ''
        else:
            pos_str = '<b>' + ', '.join(unabbr_pos_list) + ':|' + '</b>'
        # Make list of misc, field, and s_inf:
        tags_list = misc_main_list[i_0][i_1] + field_main_list[i_0][i_1]
        tags_list = [tag_dict[i_2] for i_2 in tags_list]
        tags_list += s_inf_main_list[i_0][i_1]
        tags_list = ' (' + ', '.join(tags_list) + ')'
        if tags_list == ' ()':
            gloss_str = str(gloss_num) + '. ' + '; '.join(en_list[i_0][i_1])
        else:
            gloss_str = str(gloss_num) + '. ' + '; '.join(en_list[i_0][i_1]) + tags_list
        gloss_main_list.append(pos_str + gloss_str)
        gloss_num += 1
    filtered_dict['en_list_neat'].append("|".join(gloss_main_list))

## ---- Export the filtered data dictionary to a JSON we can quickly load later ---- ##

# create json object from dictionary
json_data = json.dumps(filtered_dict)
# open file for writing, "w"
file = open("JMdict_filtered.json","w")
# write json object to file
file.write(json_data)
# close file
file.close()
