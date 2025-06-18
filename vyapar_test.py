import sys
from vyapar_service import VyaparAPIService

service = VyaparAPIService()
user_id = 6981

cmd = sys.argv[1] if len(sys.argv) > 1 else "item_summary"
ids = list(map(int, sys.argv[2:])) if len(sys.argv) > 2 else []

if cmd == "item_summary":
    print(service.item_summary(user_id))
elif cmd == "party_summary":
    print(service.party_summary(user_id))
elif cmd == "transaction_summary":
    print(service.transaction_summary(user_id))
elif cmd == "item_detailed":
    print(service.item_detailed(user_id, item_ids=ids))
elif cmd == "party_detailed":
    print(service.party_detailed(user_id, party_ids=ids))
elif cmd == "transaction_detailed":
    print(service.transaction_detailed(user_id, transaction_ids=ids))
else:
    print("Invalid command")
