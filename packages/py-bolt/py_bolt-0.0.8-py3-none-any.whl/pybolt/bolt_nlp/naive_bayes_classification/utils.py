import csv


def text_preprocess(txt: str) -> str:
    pass

    return txt


def get_data_set(file_types: list, preprocess=text_preprocess, use_frequency=True) -> (list, list):
    """Get train data from raw files.
    :param file_types: like [(file_path, type), (file_path, type)]
    :param preprocess: pre process the raw txt
    :return: inputs, targets
    """
    inputs = []
    targets = []
    for file, label in file_types:
        with open(file, 'r', encoding='utf-8') as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                txt = row[0]
                if preprocess is not None:
                    txt = preprocess(txt)
                if use_frequency:
                    for _ in range(int(row[1])):
                        inputs.append(txt)
                        targets.append(label)
                else:
                    inputs.append(txt)
                    targets.append(label)
    return inputs, targets


def get_data_set_test(file_types: list):
    inputs = []
    targets = []
    for file, label in file_types:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                inputs.append(line.strip())
                targets.append(label)
    return inputs, targets