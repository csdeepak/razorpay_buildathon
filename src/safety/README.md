# safety

`policy_gateway.py` — `PolicyGateway`, four rules (category, payee_scope,
spend_cap, velocity), runs before `act` so it's preventive, not detective.
See ../README.md for depth allocation and status, and
`docs/decisions/0006-safety-layer.md` for why it's built this way.
