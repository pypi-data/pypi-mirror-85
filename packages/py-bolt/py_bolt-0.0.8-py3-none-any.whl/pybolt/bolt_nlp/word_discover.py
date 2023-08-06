"""
Discover and extract dictionaries from massive corpus
"""
from pybolt.utils import package_path
from pybolt.utils import default_logger as logging
from pybolt.bolt_text import bolt_text
from collections import Counter
from tqdm import tqdm
import struct
import os
import time
import re
import math

default_pattern = re.compile("([^\u4E00-\u9FD5\u9FA6-\u9FEF\u3400-\u4DB5a-zA-Z0-9 +]+)", re.U)

settings = {
    "corpus_name": "corpus.txt",
    "char_vocab_name": "char_vocab.txt",
    "ngram_counts_result": "ngram_counts.b",
    "ngram_counts_result_txt": "ngram_counts.txt",
    "ngram_pmi": "pmi.txt",
    "target_file": "new_words.vocab"
}


class CountNgrams(object):
    """Count Ngram frequency use kenlm.
    """

    def __init__(self, n_max):
        self.n_max = n_max
        self.__cpp_tool = os.path.join(package_path, "bolt_nlp", "count_ngrams")

    def count_ngrams(self, source_corpus_file, write_vocab_file, write_results_file, memory="50%"):
        """use os.system call Kenlm's count_ngrams count ngrams frequency
                    Counts n-grams from standard input.
                    corpus count:
                        -h [ --help ]                     Show this help message
                        -o [ --order ] arg                Order
                        -T [ --temp_prefix ] arg (=/tmp/) Temporary file prefix
                        -S [ --memory ] arg (=80%)        RAM
                        --read_vocab_table arg            Vocabulary hash table to read.  This should
                                                          be a probing hash table with size at the beginning.
                        --write_vocab_list arg            Vocabulary list to write as null-delimited strings.
        """
        executive_code = self.__cpp_tool + f' -S {memory} -o {self.n_max} --write_vocab_list {write_vocab_file} < {source_corpus_file} > {write_results_file}'
        print(executive_code)
        status = os.system(executive_code)
        if status == 0:
            return 'Success,code is : %s , \n code is : %s ' % (status, executive_code)
        else:
            return 'Fail,code is : %s ,\n code is : %s ' % (status, executive_code)

    def read_ngrams(self, char_vocab, ngrams_result_file):
        """reference https://github.com/kpu/kenlm/issues/201
        """

        def unpack(t, s):
            return struct.unpack(t, s)[0]

        with open(char_vocab) as f:
            chars = f.read()
        chars = chars.split('\x00')
        chars = [i for i in chars]  # .decode('utf-8')
        # read ngrams
        ngrams = [Counter() for _ in range(self.n_max)]
        total = 0
        size_per_item = self.n_max * 4 + 8
        with open(ngrams_result_file, 'rb') as f:
            filedata = f.read()
            filesize = f.tell()
        logging.info("Read the count results...")
        for i in tqdm(range(0, filesize, size_per_item)):
            s = filedata[i: i + size_per_item]
            n = unpack('l', s[-8:])
            total += n

            c = [unpack('i', s[j * 4: (j + 1) * 4]) for j in range(self.n_max)]
            c = ''.join([chars[j] for j in c if j > 2])
            for j in range(len(c)):
                ngrams[j][c[:j + 1]] += n
        return ngrams, total


class SimpleTrie:
    """Trie tree structure: used to search the continuous fragments made up of ngrams
    """

    def __init__(self):
        self.root = {}
        self.end = -1

    def insert(self, word):
        """Insert a word into the trie
        """
        curNode = self.root
        for c in word:
            if c not in curNode:
                curNode[c] = {}
            curNode = curNode[c]
        curNode[self.end] = True

    def tokenize(self, sentence):
        result = []
        start, end = 0, 1
        for i, c1 in enumerate(sentence):
            curNode = self.root
            if i == end:
                word = sentence[start: end]
                result.append(word)
                start, end = i, i + 1
            for j, c2 in enumerate(sentence[i:]):
                if c2 in curNode:
                    curNode = curNode[c2]
                    if self.end in curNode:
                        if i + j + 1 > end:
                            end = i + j + 1
                else:
                    break
        result.append(sentence[start: end])
        return result

    def search(self, word):
        curNode = self.root
        for c in word:
            if c not in curNode:
                return False
            curNode = curNode[c]
        # not end
        if self.end not in curNode:
            return False
        return True

    def max_match_cut(self, sentence, reverse=True):
        result = []
        i = len(sentence)
        if reverse:
            while i > 0:
                for j in range(0, i):
                    if self.search(sentence[j: i]) or i - j == 1:
                        result.append(sentence[j: i])
                        i = j
                        break
            return result[::-1]
        while i < len(sentence):
            max_index = i
            curNode = self.root
            for j in range(i, len(sentence)):
                if sentence[j] in curNode:
                    curNode = curNode[sentence[j]]
                    if self.end in curNode:
                        max_index = j
                else:
                    break
            result.append(sentence[i: max_index + 1])
            i = max_index + 1
        return result


class WordDiscover(object):
    """

    """

    def __init__(self, task_name="word-discover", min_pmi: list = [0, 2, 4, 6], min_count=32):
        self.__run_at = str(int(time.time()))
        self.__save_path = f"./{task_name}-results/{self.__run_at}"
        self.__cn = CountNgrams(len(min_pmi))
        self.__candidate_trie = SimpleTrie()
        self.valid_ngrams = None
        self.candidates = None
        self.__min_pmi = min_pmi
        self.__min_count = min_count
        os.makedirs(self.__save_path)

    def generate_corpus(self, files: list, normalized_number=False):
        def corpus():
            for file in files:
                with open(file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = bolt_text.clean(line,
                                               my_pattern=default_pattern,
                                               pattern_replace=" ",
                                               normalize=True,
                                               crc_cut=3,
                                               num_normal=normalized_number)
                        if line:
                            yield line

        with open(os.path.join(self.__save_path, "corpus.txt"), 'w', encoding='utf-8') as f:
            logging.info("Generate corpus...")
            for line in tqdm(corpus()):
                f.write(' '.join(line) + '\n')

    def count_ngrams(self, memory="50%", save_txt=True):
        self.__cn.count_ngrams(source_corpus_file=os.path.join(self.__save_path, settings["corpus_name"]),
                               write_vocab_file=os.path.join(self.__save_path, settings["char_vocab_name"]),
                               write_results_file=os.path.join(self.__save_path, settings["ngram_counts_result"]),
                               memory=memory)
        ngrams, total = self.__cn.read_ngrams(char_vocab=os.path.join(self.__save_path, settings["char_vocab_name"]),
                                              ngrams_result_file=os.path.join(self.__save_path,
                                                                              settings["ngram_counts_result"]))
        if save_txt:
            with open(os.path.join(self.__save_path, settings["ngram_counts_result_txt"]), 'w', encoding='utf-8') as f:
                for ngram in ngrams:
                    for word, wf in ngram.items():
                        f.write(f"{word} {wf}\n")
        return ngrams, total

    def __filter_ngrams(self, ngrams, total):
        """filter the low pmi parts.
        Generate the candidate trie.
        """
        logging.info("Filter the ngrams by pmi, and create the candidate trie... ")
        output_ngrams = Counter()
        with open(os.path.join(self.__save_path, settings["ngram_pmi"]), 'w', encoding='utf-8') as pmi_file:
            for i in range(self.__cn.n_max - 1, 0, -1):
                for w, v in ngrams[i].items():
                    pmi = min(
                        [total * v / (ngrams[j].get(w[:j + 1], total) * ngrams[i - j - 1].get(w[j + 1:], total))
                         for j in range(i)])
                    if math.log(pmi) >= self.__min_pmi[i]:
                        output_ngrams[w] = v
                        self.__candidate_trie.insert(w)
                    pmi_file.write(f"{w}\t{pmi}\n")
        self.valid_ngrams = output_ngrams

    def __expansion_filter(self, remove_single_char=True):
        """Extend the vocabulary using the longest match principle,and twice filter.
        """

        n_max = self.__cn.n_max
        valid_ngrams = self.valid_ngrams

        def twice_filter(candidates):
            """filter the candidates keep the high mi ngrams
            :param candidates: the candidate words
            """
            result = Counter()
            for i, j in candidates.items():
                if len(i) < 3:
                    result[i] = j
                elif len(i) <= n_max and i in valid_ngrams:
                    result[i] = j
                elif len(i) > n_max:
                    flag = True
                    for k in range(len(i) + 1 - n_max):
                        if i[k: k + n_max] not in valid_ngrams:
                            flag = False
                    if flag:
                        result[i] = j
            return result

        candidates = Counter()
        logging.info("Start generate the candidates...")
        with open(os.path.join(self.__save_path, settings["corpus_name"]), 'r', encoding='utf-8') as f:
            for line in tqdm(f):
                line = "".join(line.strip().split())
                for w in self.__candidate_trie.tokenize(line.strip()):
                    # remove single char
                    if remove_single_char and len(w) < 2:
                        continue
                    candidates[w] += 1
        # filter by word frequency
        candidates = {i: j for i, j in candidates.items() if j >= self.__min_count}
        logging.info("Complete candidates by frequency.")

        # filter by high mutual information ngrams
        candidates = twice_filter(candidates)
        logging.info("Complete filter by mutual information of ngrams")
        logging.info("Generate word candidates successful!")
        self.candidates = candidates
        del candidates

    def __save(self):
        with open(os.path.join(self.__save_path, settings["target_file"]), 'w', encoding='utf-8') as f:
            for i, j in sorted(self.candidates.items(), key=lambda x: -x[1]):
                s = '%s %s\n' % (i, j)
                f.write(s)
        logging.info(f"Save vocab successfully: {os.path.join(self.__save_path, settings['target_file'])}")

    def word_discover(self, txts: list,
                      normalized_number: bool = True,
                      remove_single_char: bool = True,
                      memory: str = "50%",
                      save_ngram_counts_txt: bool = True):
        """
            discover the word from corpus
        """
        self.generate_corpus(txts, normalized_number)
        ngrams, total = self.count_ngrams(memory=memory, save_txt=save_ngram_counts_txt)
        self.__filter_ngrams(ngrams, total)
        self.__expansion_filter(remove_single_char=remove_single_char)
        self.__save()

