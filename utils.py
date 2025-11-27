import re
from pyxdameraulevenshtein import damerau_levenshtein_distance


class LexicalEntry:
    """LexicalEntry class represents a unit of information about a word and its potential error."""

    def __init__(self, word='', error=''):
        """
        Initializes a LexicalEntry object with a correct 'word' and an optional 'error' word.

        Parameters:
        - word (str): The correct word.
        - error (str): The error word (default is an empty string if not provided).
        """
        self.word = word  # initialize word attribute with the provided word
        self.error = error  # initialize error attribute with the provided error (or an empty string if not provided)

    # Method to create a new LexicalEntry object with an empty error attribute
    def fixError(self):
        """
        Creates a new LexicalEntry object with the same correct word but an empty error attribute.

        Returns:
        - LexicalEntry: A new LexicalEntry object with an empty error attribute.
        """
        return LexicalEntry(self.word, '')

    # Method to check if the LexicalEntry object has an error
    def hasError(self):
        """
        Checks if the LexicalEntry object has an error.

        Returns:
        - bool: True if the LexicalEntry object has an error, otherwise False.
        """
        if self.error:
            return True
        else:
            return False

    # Method to check if the error is within edit distance one and contains no numerics/punctuation
    def isValidTest(self):
        """
        Returns true if the error is within edit distance one and contains no numerics/punctuation.
        False otherwise.

        Returns:
        - bool: True if the error is within edit distance one and contains no numerics/punctuation,
                otherwise False.
        """
        if not self.hasError():
            return False
        # Calculate the Damerau-Levenshtein distance between the correct word and the error word
        distance = damerau_levenshtein_distance(self.word, self.error)
        if distance > 1:
            return False
        regex = '.*[^a-zA-Z].*'  # Regular expression to match any non-alphabetic characters
        if re.match(regex, self.word) or re.match(regex, self.error):
            return False
        return True

    # Method to create a string representation of the LexicalEntry object
    def __str__(self):
        """
        Returns a formatted string representation of the LexicalEntry object.

        Format: word (error)?

        Returns:
        - str: A string representation of the LexicalEntry object.
        """
        rep = self.word
        if self.hasError():
            rep = rep + " (" + self.error + ")"
        return rep


class Sentence:
    """Contains a list of LexicalEntries."""

    def __init__(self, sentence=None):
        """
        Initializes a Sentence object with a list of LexicalEntries.

        Parameters:
        - sentence (list): A list of LexicalEntries (default is an empty list if not provided).
        """
        if sentence == None:
            self.data = []
        elif type(sentence) == list:
            self.data = list(sentence)
        else:
            self.data = list(sentence.data)

    def get_error_sentence(self):
        """
        Returns a list of strings with the sentence containing all errors.

        Returns:
        - list: A list of strings representing the sentence with errors.
        """
        errorSentence = []
        for lexical_entry in self.data:
            if lexical_entry.hasError():
                errorSentence.append(lexical_entry.error)
            else:
                errorSentence.append(lexical_entry.word)
        return errorSentence

    def get_correct_sentence(self):
        """
        Returns a list of strings with the sentence containing all corrections.

        Returns:
        - list: A list of strings representing the sentence with corrections.
        """
        correctSentence = []
        for lexical_entry in self.data:
            correctSentence.append(lexical_entry.word)
        return correctSentence

    def is_correction(self, candidate):
        """
        Checks if a list of strings is a correction of this sentence.

        Parameters:
        - candidate (list): A list of strings to check for correction.

        Returns:
        - bool: True if the candidate is a correction, otherwise False.
        """
        if len(self.data) != len(candidate):
            return False
        for i in range(len(self.data)):
            if candidate[i] != self.data[i].word:
                return False
        return True

    def get_error_index(self):
        """
        Returns the index of the first error in the sentence, or -1 if there is no error.

        Returns:
        - int: Index of the first error or -1 if there is no error.
        """
        for i in range(0, len(self.data)):
            if self.data[i].hasError():
                return i
        return -1

    def get(self, i):
        """
        Returns the lexical_entry at the specified index.

        Parameters:
        - i (int): Index of the lexical_entry to retrieve.

        Returns:
        - lexical_entry: The lexical_entry at the specified index.
        """
        return self.data[i]

    def update(self, i, lexical_entry):
        """
        Updates the lexical_entry at the specified index with a new value.

        Parameters:
        - i (int): Index of the LexicalEntry to update.
        - val (lexical_entry): New lexical_entry value.
        """
        self.data[i] = lexical_entry

    def clean_sentence(self):
        """
        Returns a new sentence with all lexical_entry instances having errors removed.

        Returns:
        - Sentence: A new Sentence object with errors removed.
        """
        sentence = Sentence()
        for lexical_entry in self.data:
            clean = lexical_entry.fixError()
            sentence.append(clean)
        return sentence

    def is_empty(self):
        """
        Checks if the sentence is empty.

        Returns:
        - bool: True if the sentence is empty, otherwise False.
        """
        return len(self.data) == 0

    def append(self, lexical_entry):
        """
        Appends a lexical_entry to the sentence.

        Parameters:
        - item (lexical_entry): The lexical_entry to append to the sentence.
        """
        self.data.append(lexical_entry)

    def __len__(self):
        """
        Returns the length of the sentence using the len() function.

        Returns:
        - int: The length of the sentence.
        """
        return len(self.data)

    def __str__(self):
        """
        Returns a string representation of the Sentence object.

        Returns:
        - str: A string representation of the Sentence object.
        """
        str_list = []
        for lexical_entry in self.data:
            str_list.append(str(lexical_entry))
        return ' '.join(str_list)


class Corpus:
    """
    Represents a corpus of sentences, with methods for processing and generating test cases.
    """

    corpus = []  # List of sentences

    def __init__(self, filename=None):
        """
        Initializes a Corpus object.

        Parameters:
        - filename (str): The name of the file containing the dataset (default is None).
        """
        if filename:
            self.read_corpus(filename)
        else:
            self.corpus = []

    def read_corpus(self, filename):
        """
        Reads in Corpus data from a file and processes it into a list of Sentences.

        Parameters:
        - filename (str): The name of the file containing the dataset.
        """
        f = open(filename)
        self.corpus = []

        for line in f:
            sentence = self.process_line(line)
            if sentence:
                self.corpus.append(sentence)

    def process_line(self, line):
        """
        Processes a line from the Corpus dataset, extracting tokens and creating a Sentence object.

        Parameters:
        - line (str): A line from the Corpus dataset.

        Returns:
        - Sentence: A processed Sentence object.
        """
        # Stripping, lowercasing, and removing punctuation from the line
        line = line.strip().lower().replace('"', '').replace(',', '').replace('.', '').replace('!', '') \
            .replace("'", '').replace(":", '').replace(";", '')

        if line == '':
            return None

        processed_tokens = Sentence()
        processed_tokens.append(LexicalEntry("<s>"))  # Start symbol

        tokens = line.split()
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token == '<err':
                targ = tokens[i + 1]
                targ_splits = targ.split('=')
                correct_token = targ_splits[1][:-1]  # Chop off the trailing '>'
                correct_token_splits = correct_token.split()

                if len(correct_token_splits) > 2:  # Target with multiple words
                    for correct_word in correct_token_splits:
                        processed_tokens.append(LexicalEntry(correct_word))
                elif tokens[i + 3] != '</err>':
                    processed_tokens.append(LexicalEntry(correct_token))
                else:
                    incorrect_token = tokens[i + 2]
                    processed_tokens.append(LexicalEntry(correct_token, incorrect_token))

                i += tokens[i:].index('</err>') + 1  # Update index
            else:  # Regular word
                processed_tokens.append(LexicalEntry(token))
                i += 1

        processed_tokens.append(LexicalEntry("</s>"))
        return processed_tokens

    def generate_test_cases(self):
        """
        Returns a list of sentences with exactly one eligible spelling error.

        Returns:
        - list: A list of Sentences with eligible spelling errors.
        """
        testCases = []  # List of Sentences

        for sentence in self.corpus:
            clean_sentence = sentence.clean_sentence()

            for i in range(0, len(sentence)):
                lexical_entry_i = sentence.get(i)

                if lexical_entry_i.hasError() and lexical_entry_i.isValidTest():
                    testSentence = Sentence(clean_sentence)
                    testSentence.update(i, lexical_entry_i)
                    testCases.append(testSentence)

        return testCases

    def get_vocabulary(self):
        """
        Retrieves the vocabulary from the Corpus object.

        Returns:
        - set: A set containing unique words from the corpus.
        """
        vocabulary = set()
        for sentence in self.corpus:
            for word in sentence.data:
                vocabulary.add(word.word)
        return vocabulary

    def __str__(self):
        """
        Returns a string representation of the Corpus object.

        Returns:
        - str: A string representation of the Corpus object.
        """
        str_list = []
        for sentence in self.corpus:
            str_list.append(str(sentence))
        return '\n'.join(str_list)


class SpellingResult:
    numCorrect = 0
    numTotal = 0

    def __init__(self):
        self.numCorrect = 0
        self.numTotal = 0

    def __init__(self, correct, total):
        self.numCorrect = correct
        self.numTotal = total

    def get_accuracy(self):
        if self.numTotal == 0:
            return 0.0
        else:
            return float(self.numCorrect) / self.numTotal

    def __str__(self):
        return (f'Correct: {self.numCorrect}, Total: {self.numTotal}, Accuracy: {self.get_accuracy():.4%}')


def group_n_words(sentence, n):
    """
    Groups words in a given sentence into sets of 'n' consecutive words.

    Parameters:
    - sentence (list): A list of strings representing the input sentence.
    - n (int): The number of consecutive words to group together.

    Returns:
    - list: A list containing grouped words, where each group consists of 'n' consecutive words.

    Example Usage:
    >>> example = ['<s>', 'my', 'mum', 'goes', 'out', 'sometimes', '</s>']
    >>> print(group_n_words(example, 2))
    ['<s> my', 'my mum', 'mum goes', 'goes out', 'out sometimes', 'sometimes </s>']

    >>> test = ['<s>', 'my', 'mum', 'goes', 'out', 'sometimes', '</s>']
    >>> print(group_n_words(test, 3))
    ['<s> my mum goes', 'my mum goes out', 'mum goes out sometimes', 'goes out sometimes </s>']
    """
    output = []
    cart = ""

    for j in range(len(sentence)):
        k = j
        while (k < j + n and k < len(sentence)):
            # Concatenate words with proper handling for string or object type
            if type(sentence[k]) == str:
                cart += sentence[k] + ' '
            else:
                cart += sentence[k].word + ' '
            k += 1
        output.append(cart.strip())
        cart = ""
        j -= (n - 1)
    return output[:-(n - 1)]
