# ngrok Pricing Clarification

## Pricing Model

ngrok uses **subscription pricing** - NOT per-call/request charges.

### How It Works

**✅ Fixed Monthly Fee:**
- Pay once per month (or year)
- No per-request charges
- No per-call fees
- Unlimited requests (within plan limits)

**❌ NOT Pay-Per-Use:**
- Not like AWS Lambda (pay per invocation)
- Not like API services (pay per call)
- Just a flat monthly subscription

## Current Plans (as of 2024)

### Free Plan
- $0/month
- Random URLs
- 2-hour session limit (with authtoken)
- Basic features

### Starter Plan
- ~$8-10/month
- Static domain
- No session limits
- More stable

### Pro Plan
- ~$20-30/month
- More features
- Better performance

## What You Pay For

**Monthly subscription includes:**
- ✅ Static domain (if paid plan)
- ✅ Unlimited tunnel time
- ✅ Unlimited requests/calls
- ✅ Better reliability

**You DON'T pay:**
- ❌ Per HTTP request
- ❌ Per API call
- ❌ Per tool invocation
- ❌ Per ChatGPT interaction

## Example

If you pay $10/month:
- Make 1 call = $10/month
- Make 1,000 calls = $10/month
- Make 1,000,000 calls = $10/month

**Same price!** (as long as within plan limits)

## Important Notes

1. **Bandwidth limits** may apply (usually generous)
2. **Rate limits** may apply (usually high enough)
3. **No hidden per-call fees**

## Bottom Line

✅ **Fixed monthly fee** - no per-call charges
✅ **Pay once, use unlimited** (within plan limits)
✅ **Predictable cost** - same price every month

For your use case (MCP server), you'll likely never hit limits, so it's effectively unlimited for a fixed price.
