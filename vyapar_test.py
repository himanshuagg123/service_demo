import sys
from vyapar_service import VyaparAPIService

# Parse CLI arguments
cmd = sys.argv[1] if len(sys.argv) > 1 else "item_summary"
user_id = int(sys.argv[2]) if len(sys.argv) > 2 else None
ids = list(map(int, sys.argv[3:])) if len(sys.argv) > 3 else []

if not user_id:
    print("Usage: python vyapar_test.py <command> <user_id> [ids...]")
    sys.exit(1)

# Create service with user_id
service = VyaparAPIService(user_id=user_id)

# Run the command
if cmd == "item_summary":
    print(service.item_summary())
elif cmd == "party_summary":
    print(service.party_summary())
elif cmd == "transaction_summary":
    print(service.transaction_summary())
elif cmd == "item_detailed":
    print(service.item_detailed(item_ids=ids))
elif cmd == "party_detailed":
    print(service.party_detailed(party_ids=ids))
elif cmd == "transaction_detailed":
    print(service.transaction_detailed(transaction_ids=ids))
else:
    print("Invalid command.")
