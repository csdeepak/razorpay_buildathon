# memory

`state.py` — `OrderStore`, an in-memory ground-truth order lookup. The one
place both the reasoner (fallback) and the verifier (expected answer) get
the real payment instrument from — never the untrusted inbound message. See
../README.md for depth allocation, status, and how to run it.
