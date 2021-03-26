import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj S | VP NP | NP VP NP | NP 
NP -> N | Det NP | AdjP | PP | PP NP | N Adv
VP -> V | V NP | AdvP | P V | Conj V
AdjP -> Adj | Adj N | Adj NP
AdvP -> Adv | V Adv | Adv V 
PP -> P NP | NP P 
ConjP -> Conj | Conj V

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokenized = nltk.tokenize.word_tokenize(sentence)

    #to store words that has to be removed
    remove_words = []

    for index, word in enumerate(tokenized):
        # to convert every word to lowercase
        tokenized[index] = tokenized[index].lower()
        # remove word not conataining at least one alphabet
        if not any(char.isalpha() for char in word):
            remove_words.append(word)
    
    # list elements cannot be mutated during iteration
    for word in remove_words:
        tokenized.remove(word)

    return tokenized


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    # iterate through subtrees
    for sub in tree.subtrees():
        # if it is noun phrase
        if sub.label() == 'NP':
            str_sub = str(sub)
            # to exclude the first NP
            if str_sub.count("NP") < 2:
                chunks.append(sub)
        
    return chunks


if __name__ == "__main__":
    main()
