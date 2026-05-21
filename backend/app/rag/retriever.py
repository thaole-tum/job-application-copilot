import math
import re
from dataclasses import dataclass
from typing import List


TOKEN_RE = re.compile(r"[a-zA-Z0-9_+#\.-]+")


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


def _chunk_text(text: str, chunk_size: int = 900, overlap: int = 150) -> List[str]:
    cleaned = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not cleaned:
        return []
    chunks: List[str] = []
    start = 0
    step = max(1, chunk_size - overlap)
    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_size)
        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(cleaned):
            break
        start += step
    return chunks


@dataclass
class RetrievedChunk:
    source: str
    text: str
    score: float


class SimpleRAGRetriever:
    def __init__(self, chunk_size: int = 900, overlap: int = 150):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self._chunks: List[dict] = []

    def add_document(self, source: str, text: str) -> None:
        for chunk in _chunk_text(text, self.chunk_size, self.overlap):
            tokens = _tokenize(chunk)
            if not tokens:
                continue
            tf: dict = {}
            for token in tokens:
                tf[token] = tf.get(token, 0) + 1
            self._chunks.append(
                {
                    "source": source,
                    "text": chunk,
                    "tf": tf,
                    "length": len(tokens),
                }
            )

    def retrieve(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        query_terms = _tokenize(query)
        if not query_terms or not self._chunks:
            return []

        df: dict = {}
        for chunk in self._chunks:
            seen = set(chunk["tf"].keys())
            for term in seen:
                df[term] = df.get(term, 0) + 1

        n = len(self._chunks)
        avg_len = sum(c["length"] for c in self._chunks) / max(n, 1)
        k1 = 1.5
        b = 0.75

        scored: List[RetrievedChunk] = []
        for chunk in self._chunks:
            score = 0.0
            for term in query_terms:
                tf = chunk["tf"].get(term, 0)
                if tf == 0:
                    continue
                term_df = df.get(term, 0)
                idf = math.log(1 + (n - term_df + 0.5) / (term_df + 0.5))
                denom = tf + k1 * (1 - b + b * (chunk["length"] / max(avg_len, 1)))
                score += idf * ((tf * (k1 + 1)) / max(denom, 1e-9))
            if score > 0:
                scored.append(
                    RetrievedChunk(source=chunk["source"], text=chunk["text"], score=score)
                )

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]


def format_context_blocks(chunks: List[RetrievedChunk]) -> str:
    if not chunks:
        return "No relevant context retrieved."
    lines: List[str] = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(f"[{i}] source={chunk.source} score={chunk.score:.3f}")
        lines.append(chunk.text)
        lines.append("")
    return "\n".join(lines).strip()

