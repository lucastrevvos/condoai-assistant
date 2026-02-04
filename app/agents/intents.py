from enum import Enum

class Intent(str, Enum):
    SUPPORT = "support"
    FINANCE = "finance"
    DOCS = "docs"
    UNKNOWN = "unknown"