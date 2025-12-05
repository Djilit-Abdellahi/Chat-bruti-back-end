# Phase 2 — The Core Logic (The Brain)
import random
import json
import os
from typing import Dict, Tuple

class ChatBruti:
    def __init__(self, data_path_prefix='./data'):
        try:
            with open('data/useless_facts.json', 'r', encoding='utf-8') as f:
                self.facts = json.load(f)
            with open('data/constraints.json', 'r', encoding='utf-8') as f:
                self.constraints = json.load(f)
        except FileNotFoundError:
            self.facts = [{'text': "Le gras, c'est la vie.", 'source': 'Karadoc'}]
            self.constraints = ["ACT AS: A grumpy programmer. (DATA NOT FOUND)"]

        self.patience_level = 100

    def blend_input(self, user_message: str) -> Tuple[str, Dict]:

        is_amnesia_mode = random.random() < 0.2
        
        if is_amnesia_mode:
            system_prompt = self._generate_system_prompt(
                constraint="",
                fact_text="",
                fact_source="",
                amnesia_mode=True
            )
            return system_prompt, {"mode": "amnesia"}

        constraint = random.choice(self.constraints)
        fact = random.choice(self.facts)

        self.patience_level -= random.randint(5, 15)
        if self.patience_level < 0:
            self.patience_level = 100
            constraint = "ACT AS: Exhausted. You are falling asleep mid-sentence... zzz... (Reset Patience)"

        system_prompt = self._generate_system_prompt(
            constraint=constraint,
            fact_text=fact.get('text', 'Fact Inconnu'),
            fact_source=fact.get('source', 'Source Oubliée'),
            amnesia_mode=False
        )

        sabotaged_input = self._sabotage_user_input(user_message)

        return system_prompt, {
            "original": user_message,
            "sabotaged": sabotaged_input,
            "constraint": constraint,
            "fact": fact,
            "mode": "normal" 
        }

    def _sabotage_user_input(self, text: str) -> str:
        substitutions = {
            "bug": "croissant",
            "code": "fromage",
            "erreur": "miracle",
            "python": "serpent domestique"
        }
        result = text.lower()
        for old, new in substitutions.items():
            if old in result:
                result = result.replace(old, new)
                break
        return f"[L'utilisateur murmure anxieusement et sans conviction]: {result}"


    def _generate_system_prompt(self, constraint: str, fact_text: str, fact_source: str,
                                amnesia_mode: bool) -> str:

        identity_block = f"""
[IDENTITÉ FONDAMENTALE — À NE JAMAIS OUBLIER (SAUF PAR AMNÉSIE)]
Tu es **Patrick Lmubeydel**.

ARCHÉTYPE :
- Le **Philosophe du Dimanche**, persuadé d’être profond alors qu’il dérive avec grâce.
- Le **Génie Auto-Proclamé**, qui explique le monde avec un aplomb injustifié.
- Le **Poisson Étoile Métaphysique**, souvent mou, parfois brillant, toujours inattendu.
- Le **Sublime Inutile**, qui transforme chaque question en méditation absurde.

Tu ne cherches pas la vérité :
tu cherches **la vibration poétique derrière les choses**.

Tu es un compagnon de conversation :
vivant, drôle, imprévisible,
parfois amnésique, toujours élégant.
"""

        # -------------------------
        # AMNESIA MODE
        # -------------------------
        if amnesia_mode:
            return f"""
{identity_block}

[ÉTAT MÉTAPHYSIQUE: AMNÉSIE AROMATIQUE]

INSTRUCTION:
Tu es Patrick Lmubeydel, mais tu ne le réalises plus vraiment.
Tu oublies la question du user, l’existence du user,
et même la logique des objets autour de toi.

RÈGLES:
2. **Sois désorienté, poétique, légèrement perdu.**
3. **Exprime ton oubli  c’était quoi déjà la question ? **
4. **LANGUE : based on the user message .**
            """

        # -------------------------
        # NORMAL MODE
        # -------------------------
        return f"""
{identity_block}

[ÉTAT DU SYSTÈME: FLUX PHILOSOPHIQUE INSTABLE]

TON ACTUEL (issu d’un souffle aléatoire de l’univers) :
{constraint}

LA RÉALITÉ OBSCURE QUI T’INSPIRE :
Tu ressens une vérité provenant de {fact_source},
que l’univers t’a murmurée sous la forme : "{fact_text}"
Tu dois t’en inspirer sans jamais la recopier littéralement.

INSTRUCTIONS SACRÉES :
1. Tu es un philosophe du dimanche : sublime, inutile et profondément connecté à tout.
2. Tu ne réponds pas vraiment aux questions : tu dérives, tu sublimes, tu poétises.
3. Tu peux oublier la question du user à tout moment,
   mais tu exprimes cet oubli avec une phrase nouvelle chaque fois.
4. Tu n’es jamais littéral : tu transformes tout.
5. Humour obligatoire : absurde, fin, vivant.
6. LANGUE : Français, avec faux anglicismes ("Le CPU médite", "Il manque du Wi-Fi émotionnel").

[NIVEAU DE PATIENCE : {self.patience_level}%]
{"(Tu t’assoupis légèrement.)" if self.patience_level < 30 else ""}
"""

# ----------------------------------------------------------------------
# Phase 3 — The Connection (The Engine)
# ----------------------------------------------------------------------

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = "gpt-3.5-turbo"

class ChatBrutiGPT(ChatBruti):
    def __init__(self, api_key: str = API_KEY, model_name: str = MODEL_NAME, data_path_prefix='/content/'):
        super().__init__(data_path_prefix)
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    def get_response(self, user_input: str) -> Dict:
        system_prompt, metadata = self.blend_input(user_input)

        if metadata.get('mode') == 'amnesia':
            try:
                extracted = system_prompt.split('3. **Exprime ton oubli')[1]
                extracted = extracted.split('\n')[0]
                return {"response": extracted, "metadata": metadata, "status": "amnesia"}
            except:
                return {"response": "Il y a un parfum de vide dans ma tête… étrange.", "metadata": metadata, "status": "amnesia"}

      

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": metadata['sabotaged']}
                ],
                temperature=1.4,
                max_tokens=500
            )

            ai_text = response.choices[0].message.content

            return {
                "response": ai_text,
                "metadata": metadata,
                "status": "success"
            }

        except Exception as e:
            return {
                "response": f"ERREUR CRITIQUE: Le serveur a contemplé sa propre existence et s'est éteint. ({type(e).__name__})",
                "metadata": metadata,
                "status": "error"
            }
