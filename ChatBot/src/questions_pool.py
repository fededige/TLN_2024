import question

q1 = question.Question("What are the 6 remarkable phenomena of the human dialogue?",
                       ["Turns", "Speech acts", "Grounding", "Dialogue structure", "Initiative", "Implicature"],
                       3, ["Monologuing", "Incoherence", "Engagement", "Tone", "Politeness"])
q2 = question.Question("What is a Probabilistic CFG?", ["probability", "production", "CFG"], 2,
                       ["deterministic", "non-probabilistic", "context-sensitive"])
q3 = question.Question("Is the MALT algorith a 'dependency parser' or a 'constituent parser'?", ["dependencies parser"], 1,
                       ["constituents parser", "phrase structure parser", "treebank parser"])
q4 = question.Question("What is POS Tagging?", ["grammatical", "ambiguity"], 2, ["syntactic", "parsing", "semantic"])
q5 = question.Question("What is the PARSEVAL measure?", ["precision", "recall", "golden tree"], 2,
                       ["golden corpus", "training data"])
q6 = question.Question("What are the NLG symbolic phases?",
                       ["sentence planning", "text planning", "linguistic realization"],
                       3, ["lexicalization", "content determination", "surface realization"])
q7 = question.Question("HMM model is generative or discriminative?", ["generative"], 1,
                       ["discriminative", "partial", "hybrid"])
q8 = question.Question("According to Chomsky's hierarchy, do natural languages fall under 'context free grammar' or 'mildly context sensitive'?", ["mildly context sensitive"], 1,
                       ["context free grammar", "regular grammar", "unrestricted grammar", "CFG"])
# add keywords

questions = [q1, q2, q3, q4, q5, q6, q7, q8]
questions_binary = [q7, q8, q3]
questions_list = [q1, q6]
questions_open = [q2, q4, q5]

# questions = [q1]
# questions_open = []
# questions_binary = [q1]
# questions_list = []
