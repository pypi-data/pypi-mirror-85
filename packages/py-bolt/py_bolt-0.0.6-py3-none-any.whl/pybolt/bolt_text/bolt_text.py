from pybolt.bolt_text.prefix_set import PrefixSet
from pybolt.bolt_text.char_clean import CharClean
import pandas as pd
from pandarallel import pandarallel
from multiprocessing import cpu_count
from typing import Iterable


class BoltText(PrefixSet, CharClean):

    def __init__(self, workers: int = cpu_count(), **kwargs):
        """
        Args:
        workers: int, cpu count use in batch operation.
        """
        PrefixSet.__init__(self)
        CharClean.__init__(self, **kwargs)
        self.workers = workers
        pandarallel.initialize(nb_workers=workers)

    @property
    def keywords(self):
        return self.get_keywords()

    @property
    def replace_map(self):
        return self.get_replace_map()

    def add_keywords(self, keywords):
        if isinstance(keywords, str):
            self.add_keyword(keywords)
        elif isinstance(keywords, list):
            self.add_keywords_from_list(keywords)

    def add_replace_map(self, replace_dict: dict):
        self.add_keywords_replace_map_from_dict(replace_dict)

    def remove_keywords(self, keywords):
        if isinstance(keywords, str):
            return self.remove_keyword(keywords)
        elif isinstance(keywords, list):
            return self.remove_keywords_from_list(keywords)

    def batch_extract_keywords(self, lines: Iterable[str], concurrency: int = 1000000):
        examples = []
        if isinstance(lines, Iterable):
            n = 0
            for line in lines:
                n += 1
                examples.append(line)
                if n % concurrency == 0:
                    yield self.__df_filter(examples)
                    examples.clear()
            if examples:
                yield self.__df_filter(examples)
        else:
            raise TypeError("Argument: `lines` should be a Iterable.")

    def batch_replace_keywords(self, lines: Iterable[str], concurrency: int = 1000000):
        examples = []
        if isinstance(lines, Iterable):
            n = 0
            for line in lines:
                n += 1
                examples.append(line)
                if n % concurrency == 0:
                    yield self.__df_replace(examples)
                    examples.clear()
            if examples:
                yield self.__df_replace(examples)

    def batch_text_processor(self, lines: Iterable[str], processor, concurrency: int = 1000000):
        """Batch processing of text data.
        Args:
            lines: a iterable data, to process
            processor: the function use in each line
            concurrency: int
        """
        examples = []
        if isinstance(lines, Iterable):
            n = 0
            for line in lines:
                n += 1
                examples.append(line)
                if n % concurrency == 0:
                    df = pd.DataFrame(examples, columns=["example"])
                    df["processor_result"] = df.example.parallel_apply(processor)
                    yield df
                    examples.clear()
            if examples:
                df = pd.DataFrame(examples, columns=["example"])
                df["processor_result"] = df.example.parallel_apply(processor)
                yield df
                examples.clear()

    def __line_extract_processor(self, line: str):
        found_words = self.extract_keywords(line)
        if found_words:
            return found_words
        return None

    def __line_replace_keywords_processor(self, line: str):
        return self.replace_keywords(line)

    def __df_filter(self, examples: Iterable[str]):
        df = pd.DataFrame(examples, columns=["example"])
        df["keywords"] = df.example.parallel_apply(self.__line_extract_processor)
        df = df[df["keywords"].notna()]
        return df

    def __df_replace(self, examples: Iterable[str]):
        df = pd.DataFrame(examples, columns=["example"])
        df["example"] = df.example.parallel_apply(self.__line_replace_keywords_processor)
        return df
