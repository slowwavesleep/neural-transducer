from typing import Tuple, List, Optional

from conllu import parse, SentenceList

KEEP_DUPLICATES = True
ORIGINAL_FORMAT = False
ALL_LOWER_CASE = True
REMOVE_SPECIAL_SYMBOLS = True
SYMBOLS_TO_REMOVE = ("_", "=")

def parse_from_file(path: str) -> SentenceList:
    with open(path) as file:
        parsed = parse(file.read())
    return parsed

def remove_symbols_helper(form: str, lemma: str, symbols: Tuple[str, ...]) -> str:
    processed_lemma = lemma
    for symbol in symbols:
        if symbol in lemma and symbol not in form and len(lemma) > 1:
            processed_lemma = processed_lemma.replace(symbol, "")
    return processed_lemma

def convert_to_triples(
        parsed_conllu: SentenceList,
        keep_duplicates: bool = False,
        original_format: bool = True,
        all_lower_case: bool = False,
        remove_special_symbols: bool = False,
        symbols_to_remove: Optional[Tuple[str, ...]] = None,
) -> List[Tuple[str, str, str]]:
    triples = list()
    for sent in parsed_conllu:
        for token in sent:
            form = token["form"]
            lemma = token["lemma"]
            if all_lower_case:
                form = form.lower()
                lemma = lemma.lower()
            if remove_special_symbols and symbols_to_remove:
                lemma = remove_symbols_helper(form, lemma, symbols_to_remove)
            feats = token["feats"]
            part_of_speech = token["upos"]
            if feats:
                feats["UPOS"] = part_of_speech
                feats_str = ";".join([f"{key}={value}" for key, value in feats.items()])
            else:
                feats_str = f"UPOS={part_of_speech}"
            if original_format:
                triple = (lemma, form, feats_str)
            else:
                triple = (form, lemma, feats_str)
            triples.append(triple)
    if keep_duplicates:
        return triples
    else:
        return list(set(triples))

def write_data(
        data_dict, keep_duplicates, original_format, all_lower_case, remove_special_symbols, symbols_to_remove
) -> None:
    for key, value in data_dict.items():
        parsed = parse_from_file(value)
        triples = convert_to_triples(
            parsed,
            keep_duplicates=keep_duplicates,
            original_format=original_format,
            all_lower_case=all_lower_case,
            remove_special_symbols=remove_special_symbols,
            symbols_to_remove=symbols_to_remove,

        )
        with open(f"data/est.{key}", "w") as file:
            for triple in triples:
                file.write("\t".join(triple) + "\n")


data = dict(
    train="UD_Estonian-EDT/et_edt-ud-train.conllu",
    dev="UD_Estonian-EDT/et_edt-ud-dev.conllu",
    test="UD_Estonian-EDT/et_edt-ud-test.conllu"
)

write_data(
    data,
    keep_duplicates=KEEP_DUPLICATES,
    original_format=ORIGINAL_FORMAT,
    all_lower_case=ALL_LOWER_CASE,
    remove_special_symbols=REMOVE_SPECIAL_SYMBOLS,
    symbols_to_remove=SYMBOLS_TO_REMOVE,
)