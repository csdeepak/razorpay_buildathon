# memory

`state.py` — `OrderStore` (in-memory ground-truth order lookup; the one
place both the reasoner's fallback and the verifier's expected answer come
from, never the untrusted inbound message) and `VelocityTracker` (records
spend for the safety gate's daily amount/count limits). See ../README.md for
depth allocation, status, and how to run it.
