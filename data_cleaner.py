import pandas
import re
import unicodedata

def standardise_sentence(sentence):
    # Convert to lowercase
    sentence = sentence.lower()
    # Remove extra whitespace
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    # Replace curly apostrophes with straight
    sentence = re.sub(r"’", "'", sentence)
    # Convert different dashes to hyphen
    sentence = re.sub(r"–|—", "-", sentence)
    # Normalise accents and special characters
    sentence = unicodedata.normalize("NFKC", sentence)
    # Remove special characters
    sentence = re.sub(r"[^\w\s.,?!]", "", sentence)
    # Normalize punctuation (e.g., remove trailing spaces before punctuation)
    sentence = re.sub(r'\s+([?.!,])', r'\1', sentence)
    return sentence


def process_sentences(english_sentences, irish_sentences):
    # Apply standardization to both English and Irish sentences
        # Could add some logic here to only add sentences of certain length
    english_sentences = [standardise_sentence(sentence) for sentence in english_sentences]
    irish_sentences = [standardise_sentence(sentence) for sentence in irish_sentences]
    # Only keep pairs where both sentences are non-empty and aligned
    aligned_pairs = [(eng, ga) for eng, ga in zip(english_sentences, irish_sentences) if eng and ga]
    # Create a DataFrame for the parallel corpus
    df = pandas.DataFrame(aligned_pairs, columns=['English', 'Irish'])
    # Append to master dataset
    try:
        master_df = pandas.read_csv('data/master_parallel_corpus.csv')
        master_df = pandas.concat([master_df, df], ignore_index=True)
    except FileNotFoundError:
        master_df = df
    # Save updated master dataset
    master_df.to_csv('data/master_parallel_corpus.csv', index=False)


def make_master_file():
    # Open and read TedTalk data files
    with open('data/TED2020.en-ga.en', 'r') as english_file, open('data/TED2020.en-ga.ga', 'r') as irish_file:
        # Reading English and Irish files as lists of sentences
        english_sentences = english_file.readlines()
        irish_sentences = irish_file.readlines()
        process_sentences(english_sentences, irish_sentences)

    # Open and read EU bookshop data files
    with open('data/EUbookshop.en-ga.en', 'r') as english_file, open('data/EUbookshop.en-ga.ga', 'r') as irish_file:
        # Reading English and Irish files as lists of sentences
        english_sentences = english_file.readlines()
        irish_sentences = irish_file.readlines()
        process_sentences(english_sentences, irish_sentences)

    # Continue for each file pair


make_master_file()



