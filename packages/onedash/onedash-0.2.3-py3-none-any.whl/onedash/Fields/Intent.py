from dataclasses import dataclass


@dataclass
class Intent:
    name: str
    is_unsubscribed_intent: bool = False
    is_misunderstanding_intent: bool = False
    is_nps_intent: bool = False
    is_non_text_intent: bool = False

    def list_of_properties(self):
        properties = []
        if self.is_misunderstanding_intent:
            properties.append('misunderstanding')
        if self.is_unsubscribed_intent:
            properties.append('unsubscribed')
        if self.is_nps_intent:
            properties.append('nps')
        if self.is_non_text_intent:
            properties.append('non_text')
        return properties
