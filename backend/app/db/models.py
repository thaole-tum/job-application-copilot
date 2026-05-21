from dataclasses import dataclass


@dataclass
class JobAnalysis:
    content: str


@dataclass
class MatchAnalysis:
    content: str


@dataclass
class ApplicationDraft:
    short_profile: str
    cover_letter: str
    full_text: str
