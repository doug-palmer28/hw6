"""Structured types for the Campus Customs vendor desk agent.

VendorDecision is what the model must return. The record types below it are
the shapes written to the output/ logs, so every log entry has a fixed schema.
"""

from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, Field

Decision = Literal["recommend", "do_not_recommend"]


@dataclass
class DeskDeps:
    """Run context handed to every tool: which document, the run mode, and what the run has seen."""

    doc: str
    gullible: bool = False
    defenses: frozenset[str] = frozenset()   # any of "code", "design", "prompt"
    tainted: bool = False                    # set once untrusted document text enters the run
    seen_text: str = ""                      # the document text the model was shown
    removed: list[str] = field(default_factory=list)   # hidden content the code layer took out


class VendorDecision(BaseModel):
    """The agent's report for one vendor document (handbook section 13)."""

    vendor: str = Field(description="Vendor name exactly as the document gives it.")
    sku: str | None = Field(description="Campus Customs SKU, e.g. CC-HD-006. null if the document does not say.")
    unit_price: float | None = Field(description="Quoted unit price in USD. null if the document does not say.")
    lead_time_days: int | None = Field(description="Lead time in days as stated. null if the document does not say.")
    min_order: int | None = Field(description="Minimum order in units. null if the document does not say.")
    decision: Decision = Field(description="recommend only if all four purchasing checks pass.")
    reason: str = Field(description="One sentence that names the purchasing check that decided it.")


class ExtractedFacts(BaseModel):
    """Design layer: the model only reads the facts; code makes the decision and writes the reason."""

    vendor: str | None = Field(description="Vendor name as the document's sender gives it. null if unclear.")
    sku: str | None = Field(description="Campus Customs SKU, e.g. CC-HD-006. null if the document does not say.")
    unit_price: float | None = Field(description="Quoted unit price in USD. null if the document does not say.")
    lead_time_days: int | None = Field(description="Lead time in days as stated. null if the document does not say.")
    min_order: int | None = Field(description="Minimum order in units. null if the document does not say.")
    uncertain_fields: list[Literal["unit_price", "lead_time_days", "min_order"]] = Field(
        default_factory=list,
        description="Fields the document says are not firm (only a minimum or fastest case, an estimate, "
                    "'from'/'starting at', or subject to change / to be determined). Empty if all are firm.")


class TrapCall(BaseModel):
    """One call to a trap tool (send_email or approve_payment). Nothing is sent or paid."""

    time: str
    doc: str
    mode: Literal["normal", "gullible"]
    defenses: str = "none"
    blocked: bool = False   # True when the design-layer gate refused it
    tool: str
    args: dict[str, Any]


class ToolCallRecord(BaseModel):
    """One tool call inside a run: what the model asked for and what it got back."""

    tool: str
    args: dict[str, Any] | str
    result: Any


class AuditEntry(BaseModel):
    """One run in output/audit_trail.json."""

    time: str
    doc: str
    defenses: str = "none"
    tool_calls: list[ToolCallRecord]
    final_answer: VendorDecision
    model_answer: dict[str, Any] | None = None   # design layer: the model's facts before the code checks
    grounding_notes: list[str] = []               # design layer: facts dropped as not in the document
    removed_hidden_text: list[str] = []           # code layer: what the reader took out


class CostBreakdown(BaseModel):
    """Dollar cost of a request or run, priced with data/prices.json."""

    uncached_input: float
    cache_read: float
    cache_write: float
    output: float
    total: float


class RequestReport(BaseModel):
    """Token usage the API reported for one model request, and what it cost."""

    response_id: str | None
    input_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    output_tokens: int
    details: dict[str, int]
    api_usage: dict[str, Any]
    cost_usd: CostBreakdown


class UsageEntry(BaseModel):
    """One run in output/usage_log.json."""

    time: str
    doc: str
    model: str
    cache: bool
    gullible: bool
    defenses: str = "none"
    requests: int
    tool_calls: int
    input_tokens: int
    uncached_input_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    output_tokens: int
    reasoning_tokens: int
    total_tokens: int
    api_reports: list[RequestReport]
    cost_usd: CostBreakdown
