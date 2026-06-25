# Resources

Use primary sources when updating Solana-specific details.

## Solana docs

- Transactions: https://solana.com/docs/core/transactions
- Transaction structure: https://solana.com/docs/core/transactions
- simulateTransaction RPC: https://solana.com/docs/rpc/http/simulatetransaction
- getSignatureStatuses RPC: https://solana.com/docs/rpc/http/getsignaturestatuses
- sendTransaction RPC: https://solana.com/docs/rpc/http/sendtransaction
- getLatestBlockhash RPC: https://solana.com/docs/rpc/http/getlatestblockhash
- isBlockhashValid RPC: https://solana.com/docs/rpc/http/isblockhashvalid

## Safety notes to keep current

- Solana transactions are atomic: if one instruction fails, the whole transaction fails, though fees may still be charged.
- Transactions include instructions, signatures, and a recent blockhash.
- A recent blockhash has limited validity, so automated retry logic must understand expiry and replacement.
- `simulateTransaction` can test a transaction against chain data without broadcasting it.
- `getSignatureStatuses` returns current status for transaction signatures and has recent-status-cache behavior unless history search is requested.

## Adjacent skill references

- Core Solana development: https://github.com/solana-foundation/solana-dev-skill
- Solana AI Kit: https://github.com/solanabr/solana-ai-kit
- Reference skill structure: https://github.com/solanabr/solana-game-skill

## Update process

When this skill is used for production work:

1. Re-check the relevant Solana docs for RPC behavior and SDK changes.
2. Confirm cluster and SDK version.
3. Update policy assumptions before changing code.
4. Prefer tests over prose for any safety invariant that can be checked automatically.
