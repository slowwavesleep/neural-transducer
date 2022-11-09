from typing import Tuple, List

from conllu import parse, SentenceList

def parse_from_file(path: str) -> SentenceList:
    with open(path) as file:
        parsed = parse(file.read())
    return parsed


def convert_to_triples(
        parsed_conllu: SentenceList, keep_duplicates: bool = False, original_format: bool = True
) -> List[Tuple[str, str, str]]:
    triples = list()
    for sent in parsed_conllu:
        for token in sent:
            form = token["form"]
            lemma = token["lemma"]
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

def write_data(data_dict, keep_duplicates, original_format) -> None:
    for key, value in data_dict.items():
        parsed = parse_from_file(value)
        with open(f"data/est.{key}", "w") as file:
            for triple in convert_to_triples(parsed, keep_duplicates=keep_duplicates, original_format=original_format):
                file.write("\t".join(triple) + "\n")


data = dict(
    train="UD_Estonian-EDT/et_edt-ud-train.conllu",
    dev="UD_Estonian-EDT/et_edt-ud-dev.conllu",
    test="UD_Estonian-EDT/et_edt-ud-test.conllu"
)

write_data(data, keep_duplicates=True, original_format=False)