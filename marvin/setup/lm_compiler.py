import tempfile
import re
import subprocess

import marvin.support.lib

def compile(abilities):
    corpus = _compile_text_corpus(abilities)
    wfreq = _text2wfreq(corpus)
    vocab = _wfreq2vocab(wfreq)
    idngram = _text2idngram(vocab, corpus)
    return _idngram2lm(idngram, vocab)
    # return _sphinx_lm_convert(lm) # TODO: get this to work

def _compile_text_corpus(abilities):
    """
        Loads all relevant sentences from given modules and put them into
        a text file for further processing.
    """
    sentences = [
        ability['query']['examples'] for _k, ability in abilities.items()]
    # flatten:
    sentences = marvin.support.lib.flatten(sentences)

    corpus_file = tempfile.NamedTemporaryFile('w+', suffix='.txt')
    for sentence in sentences:
        for split_sentence in _transform_module_sentence(sentence):
            line = _standardize_corpus_line(split_sentence)
            corpus_file.write(line)

    corpus_file.seek(0)
    return corpus_file

def _transform_module_sentence(module_sentence):
    """
        Example sentences inside modules are given with {N} placeholders
        to represent where the persona name is to be expected. Usually at
        both the beginning and end of the phrase.
        Here the encoded format is resolved.
    """
    match_count = 0

    for match in re.finditer('{N}', module_sentence):
        match_count += 1
        variant = "{0} {1} {2}".format(
            module_sentence[:match.start()], 'MARVIN',
            module_sentence[match.end():])
        yield variant

    if match_count == 0:
        yield module_sentence

def _standardize_corpus_line(line):
    """
        To be usable for the corpus file, the line is standardized by
        upcasing everything, removing unnecessary white space, and then it is
        enclosed in silence tags.
    """
    line = line.replace('{N}', '') # remove all other occurences
    line = re.sub(' +', ' ', line).strip().upper()
    return "<s> {} </s>\n".format(line)

def _text2wfreq(corpus_file):
    """
        Returns a list of every word which occurred in the text, along with
        its number of occurrences.
    """
    wfreq_file = tempfile.TemporaryFile('w+')
    corpus_file.seek(0)
    subprocess.call('text2wfreq', stdin=corpus_file, stdout=wfreq_file)
    return wfreq_file

def _wfreq2vocab(wfreq_file):
    """
        Takes a a word unigram file, as produced by text2wfreq and converts
        it to a vocabulary file.
    """
    vocab_file = tempfile.NamedTemporaryFile('w+', suffix='.vocab')
    wfreq_file.seek(0)
    subprocess.call('wfreq2vocab', stdin=wfreq_file, stdout=vocab_file)
    return vocab_file

def _text2idngram(vocab_file, corpus_file):
    """
        Takes a text stream, plus a vocabulary file, and outputs a list of
        every id n-gram which occurred in the text, along with its number of
        occurrences.
    """
    idngram_file = tempfile.NamedTemporaryFile('w+', suffix='.idngram')
    corpus_file.seek(0)
    vocab_file.seek(0)
    subprocess.call(
        'text2idngram -vocab {0} -idngram {1}'.format(
            vocab_file.name, idngram_file.name),
        stdin=corpus_file, shell=True)
    return idngram_file

def _idngram2lm(idngram_file, vocab_file):
    """
        Takes an idngram file (in either binary (by default) or ASCII (if
        specified) format), a vocabulary file, and (optionally) a context
        cues file and turns them into a language model.
    """
    vocab_file.seek(0)
    lm_file = tempfile.NamedTemporaryFile('w+', suffix='.lm')
    idngram_file.seek(0)
    ccs_file = _context_cue_file()
    ccs_file.seek(0)
    subprocess.call(
        'idngram2lm -idngram {0} -vocab {1} -arpa {2} -context {3}'.format(
            idngram_file.name, vocab_file.name, lm_file.name, ccs_file.name
        ), shell=True)
    return lm_file

def _context_cue_file():
    """
        Since version 2 idngram2lm takes an optional file that contains context
        cues. Most notably the boundary cue `<s>`.
    """
    ccs_file = tempfile.NamedTemporaryFile('w+', suffix='.ccs')
    ccs_file.write('<s>')
    return ccs_file

# TODO: Not yet working
def _sphinx_lm_convert(lm_file):
    """
        Takes a compiled language model and turns it into binary format for
        faster loading.
    """
    bin_file = tempfile.NamedTemporaryFile('w+b', suffix='.lm.bin')
    lm_file.seek(0)
    subprocess.call(
        'sphinx_lm_convert -i {0} -o {1}'.format(
            lm_file.name, bin_file.name),
        shell=True)
    print(bin_file.name)
    bin_file.seek(0)
    return bin_file
