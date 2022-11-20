import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    print(sys.argv)
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()
    


    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    transitionModel = {}
    numberLinks = len(corpus[page])
    numberFiles = len(corpus) 

    if numberLinks != 0 :
        randProb = (1 - damping_factor) / numberFiles
        specProb = damping_factor / numberLinks

    else:
        randProb = (1 - damping_factor) / numberFiles
        specProb = 0

    for f in corpus:
        if len(corpus[page]) == 0:
            transitionModel[f] = 1 / numberFiles

        else:
            if f not in corpus[page]:
                transitionModel[f] = randProb

            else:
                transitionModel[f] = specProb + randProb

    if round(sum(transitionModel.values()),5) != 1:
        print ("Incorrect. The probabilities add up to ", {sum(transitionModel.values())})
        
    return transitionModel

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samplePR = {}
    for pg in corpus:
        samplePR[pg] = 0

    sample = None
    for i in range(n):
        if sample == None:
            choices = list(corpus.keys())
            sample = random.choice(choices)
            samplePR[sample] += 1

        else:
            nextSampleProb = transition_model(corpus, sample, damping_factor)
            choices = list(nextSampleProb.keys())
            weights = [nextSampleProb[key] for key in choices]
            sample = random.choices(choices, weights).pop()
            samplePR[sample] +=1

    samplePR = {key : value / n for key, value in samplePR.items()}
    if round(sum(samplePR.values()),5) != 1:
        print ("Incorrect. The probabilities add up to ", {sum(transitionModel.values())})
    else: 
        print(f'Sum of sample_pagerank values: {round(sum(samplePR.values()),10)}')
    return samplePR

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    iteratePR = {}
    numberPg = len(corpus)

    for pg in corpus:
        iteratePR[pg] = 1/numberPg

    changes = 1
    iterations = 1
    
    while changes >= 0.001:
        changes = 0
        previousState = iteratePR.copy()
        
        for pg in iteratePR:
            parents = [link for link in corpus if pg in corpus[link]]
            first = ((1 - damping_factor)/ numberPg)
            second = []
            if len(parents) != 0:
                for parent in parents:
                    numLinks = len(corpus[parent])
                    val = previousState[parent] / numLinks
                    second.append(val)

            second = sum(second)
            iteratePR[pg] = first + (damping_factor * second)
            newChange = abs(iteratePR[pg] - previousState[pg])
            if changes < newChange:
                changes = newChange
        iterations += 1

    dictSum = sum(iteratePR.values())
    iteratePR = {key: value/dictSum for key, value in iteratePR.items()}
    print(f'\nPageRank value after {iterations} iterations.')
    print(f'Sum of iterate_pagerank values: {round(sum(iteratePR.values()),10)}')
    return iteratePR

        


if __name__ == "__main__":
    main()
