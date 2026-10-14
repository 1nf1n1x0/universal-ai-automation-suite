"""
Smart Document & Market Intelligence Synthesizer
Part of the Universal AI Agent Automation Suite.
Processes unstructured documents/market briefs into clean, actionable executive summaries.
"""

import re
import json
from typing import Dict, Any, List

class DocumentSynthesizer:
    def __init__(self):
        pass

    def extract_key_metrics(self, text: str) -> List[str]:
        # Détection de montants, pourcentages, dates et chiffres clés
        metrics = []
        currencies = re.findall(r'(\$\d+[\d,]*(?:\.\d+)?|\d+[\d,]*\s*(?:€|USD|EUR|USDC))', text)
        percentages = re.findall(r'(\d+(?:\.\d+)?%)', text)
        metrics.extend([f"Valeur financière : {c}" for c in set(currencies)])
        metrics.extend([f"Ratio/Progression : {p}" for p in set(percentages)])
        return metrics

    def extract_action_items(self, text: str) -> List[str]:
        # Détection de tâches et d'actions (TODO, must, require, action)
        actions = []
        for line in text.split("\n"):
            line = line.strip()
            if any(k in line.lower() for k in ["todo", "action", "requis", "priorité", "urgent", "étape", "step"]):
                actions.append(line)
        return actions[:10]

    def synthesize(self, title: str, raw_text: str) -> Dict[str, Any]:
        words = len(raw_text.split())
        metrics = self.extract_key_metrics(raw_text)
        actions = self.extract_action_items(raw_text)

        return {
            "title": title,
            "word_count": words,
            "key_metrics": metrics,
            "action_items": actions,
            "reading_time_minutes": round(words / 200, 1),
            "status": "Synthèse générée avec succès"
        }

if __name__ == "__main__":
    synthesizer = DocumentSynthesizer()
    sample = """
    Rapport d'audit trimestriel 2026 :
    Croissance globale de 24.5% sur le chiffre d'affaires atteignant $150,000.
    Coûts d'acquisition réduits de 12%.
    TODO: Mettre à jour l'infrastructure API d'ici vendredi.
    Action: Finaliser les intégrations des partenaires de paiement.
    Priorité: Déployer le nouveau module de monitoring.
    """
    res = synthesizer.synthesize("Audit Q3 2026", sample)
    print(json.dumps(res, indent=2, ensure_ascii=False))
