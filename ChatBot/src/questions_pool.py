import question
# What are the 6 remarkable phenomena of the human dialogue?
#


q1 = question.Question("What are the 6 remarkable phenomena of the human dialogue?",
                       [
                           "Turns",
                           "Speech acts",
                           "Grounding",
                           "Dialogue structure",
                           "Initiative",
                           "Implicature"
                       ], 3, [
                           "Monologuing",
                           "Incoherence",
                           "Engagement",
                           "Tone",
                           "Politeness"
                       ])
q2 = question.Question("What is a Probabilistic CFG?", ["two"], 2)
q3 = question.Question("What is the Frame-Based Semantics in DS?", ["three"], 2)
q4 = question.Question("What is POS Tagging?", ["four"], 2)
q5 = question.Question("What is the PARSEVAL measure?", ["five"], 2)
q6 = question.Question("What are the NLG symbolic phases?", ["six"], 3, [
                           "Monologuing",
                           "Incoherence",
                           "Engagement",
                           "Tone",
                           "Politeness"
                       ])
q7 = question.Question("What is the Referring Expression Generation task?", ["seven"], 2)
q8 = question.Question("How the CKY algorithm works?", ["eight"], 2)
q9 = question.Question("HMM model is generative or discriminative?", ["generative"], 1, ["discriminative", "partial"])

# add keywords

questions = [q1, q2, q3, q4, q5, q6, q7, q8]
questions_binary = [q9]
questions_list = [q1, q6]
questions_open = [q2, q3, q4, q5, q7, q8]
