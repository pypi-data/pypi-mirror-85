from dataclasses import dataclass


@dataclass
class Reference:
    to: str = None
    utm_source: str = None
    utm_medium: str = None
    utm_campaign: str = None
    utm_content: str = None
    utm_term: str = None
    ref: str = None
    ref_source: str = None

    def json(self):
        return {'ref': self.ref if self.ref is not None else '',
                'ref_source': self.ref_source if self.ref_source is not None else '',
                'to': self.to if self.to is not None else '',
                'utm_source': self.utm_source if self.utm_source is not None else '',
                'utm_medium': self.utm_medium if self.utm_medium is not None else '',
                'utm_campaign': self.utm_campaign if self.utm_campaign is not None else '',
                'utm_content': self.utm_content if self.utm_content is not None else '',
                'utm_term': self.utm_term if self.utm_term is not None else ''
                }
