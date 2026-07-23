# Educational and research scoring

- MCQ and TF items are scored by normalized exact match to the reference answer.
- Educational FIB and research SA responses are judged by Gemini 2.5 Pro at
  temperature 0 using a deterministic binary rubric.
- The binary rubric permits normalized exact matches, a reference phrase contained
  verbatim within a longer answer, parenthetical acronym differences, generic filler
  nouns, standard spelling/unit variants, and genuine audiology synonyms.
- Research SA responses were constrained to concise direct answers. A separate
  reference-fidelity audit and grading re-judgment are reported under
  `results/research/`.

Exact prompt JSON files are provided in `prompts/`.
