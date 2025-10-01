import re
import random

# Lire le fichier
with open('securite_poste_dev.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Définir les modifications manuellement pour chaque quiz/question
# Format: (quiz_id, question_id, new_order) où new_order est [0, 1, 2] mélangé
modifications = {
    (2, 1): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de A à C
    (2, 2): [1, 0, 2],  # B, A, C -> déplacer la bonne réponse de B à A
    (2, 3): [2, 0, 1],  # C, A, B -> déplacer la bonne réponse de B à C
    (2, 4): [2, 0, 1],  # C, A, B -> déplacer la bonne réponse de B à C
    (2, 5): [0, 2, 1],  # A, C, B -> garder B en B

    (3, 1): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de B à C
    (3, 2): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de B à A
    (3, 3): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de B à C
    (3, 4): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de A à B
    (3, 5): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de B à C

    (4, 1): [2, 0, 1],  # C, A, B -> déplacer la bonne réponse de C à A
    (4, 2): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de B à C
    (4, 3): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de B à A
    (4, 4): [2, 0, 1],  # C, A, B -> déplacer la bonne réponse de B à C
    (4, 5): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de B à A

    (5, 1): [2, 0, 1],  # C, A, B -> déplacer la bonne réponse de C à B
    (5, 2): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de C à A
    (5, 3): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de A à B
    (5, 4): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de B à A
    (5, 5): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de C à B

    (6, 1): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de B à C
    (6, 2): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de B à A
    (6, 3): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de B à C
    (6, 4): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de B à A
    (6, 5): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de B à C

    (7, 1): [2, 0, 1],  # C, A, B -> déplacer la bonne réponse de A à C
    (7, 2): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de C à B
    (7, 3): [2, 0, 1],  # C, A, B -> déplacer la bonne réponse de B à A
    (7, 4): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de A à B
    (7, 5): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de B à C

    (8, 1): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de C à B
    (8, 2): [2, 0, 1],  # C, A, B -> déplacer la bonne réponse de A à C
    (8, 3): [1, 2, 0],  # B, C, A -> déplacer la bonne réponse de B à A
    (8, 4): [2, 1, 0],  # C, B, A -> déplacer la bonne réponse de A to B
    (8, 5): [1, 0, 2],  # B, A, C -> déplacer la bonne réponse de C à A
}

# Pour chaque modification
for (quiz_id, question_id), new_order in modifications.items():
    # Trouver le bloc de la question
    pattern = rf'(<div class="quiz-question">.*?<div class="question-text">{question_id}\..*?</div>.*?<div class="quiz-options">)(.*?)(</div>.*?</div>.*?</div>)'

    def replace_answers(match):
        before = match.group(1)
        options_block = match.group(2)
        after = match.group(3)

        # Extraire les 3 réponses
        answer_pattern = r'<div class="quiz-option" onclick="selectAnswer\(' + str(quiz_id) + r', ' + str(question_id) + r', (?:true|false)\)">[A-C]\)[^<]+</div>'
        answers = re.findall(answer_pattern, options_block)

        if len(answers) != 3:
            return match.group(0)

        # Réorganiser selon new_order
        reordered = [answers[i] for i in new_order]

        # Remplacer les lettres A, B, C
        letters = ['A', 'B', 'C']
        for i in range(3):
            reordered[i] = re.sub(r'>[A-C]\)', f'>{letters[i]})', reordered[i])

        # Reconstruire le bloc
        new_options = '\n                            '.join(reordered)
        return before + '\n                            ' + new_options + '\n                        ' + after

    content = re.sub(pattern, replace_answers, content, flags=re.DOTALL)

# Sauvegarder
with open('securite_poste_dev.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Randomisation terminée avec succès!")
