# Problem 2 — Size Up the Handbook

**Model:** `gpt-6-luna`
**Document:** `data/shop_handbook.md` (sent to the model on every vendor desk call)
**Prices:** `data/prices.json`

---

## 1. Token count

| Measure | Value |
|---|---|
| **Tokens (o200k_base)** | **10,069** |
| Characters | 29,241 |
| Words | 6,127 |
| Lines | 338 |

### How I determined it

1. I loaded `data/shop_handbook.md` exactly as the agent will send it (UTF-8, no edits).
2. I tokenized it offline with OpenAI's `tiktoken` library (v0.14.0), using the `o200k_base` encoding.
   - `tiktoken` has no built-in mapping for `gpt-6-luna`.
   - OpenAI's current model family (`gpt-4o`, `gpt-5`) maps to `o200k_base`, so that is the closest tokenizer available for Luna.
3. I cross-checked the result against other methods:

| Method | Tokens | Note |
|---|---|---|
| `o200k_base` (tiktoken) | **10,069** | Used for all cost math |
| `cl100k_base` (older GPT-4 tokenizer) | 10,191 | Within about 1% |
| Rule of thumb: characters ÷ 4 | 7,310 | Undercounts by about 27% |
| Rule of thumb: words × 4/3 | 8,169 | Undercounts by about 19% |

The rules of thumb run low because most of the handbook is tables. SKUs like `CC-HD-001`, dollar amounts and `|` separators split into many short tokens.

### Where the tokens are

| Section | Tokens | Share |
|---|---:|---:|
| §9 Product catalogue | 6,923 | 68.8% |
| §10 Recent purchase orders | 1,464 | 14.5% |
| §5 Approved vendors | 419 | 4.2% |
| §4 Purchasing rules | 269 | 2.7% |
| All other sections (title, §1–3, §6–8, §11–13) | 994 | 9.9% |
| **Total** | **10,069** | **100%** |

The rules the agent actually applies (§4, §5, §6, §13) take about 900 tokens. The catalogue and purchase history make up the rest.

---

## 2. Luna prices (from `data/prices.json`)

| Price type | $ per 1M tokens | $ per token |
|---|---:|---:|
| Input (uncached) | $0.10 | $0.0000001 |
| Cache write | $0.125 | $0.000000125 |
| Cached input (cache hit) | $0.01 | $0.00000001 |
| Output | $0.50 | *(not used here: the handbook is input only)* |

Formula: **cost = tokens × (price per 1M ÷ 1,000,000)**

---

## 3. Cost without cached tokens

Every call pays the full input price for all 10,069 handbook tokens.

**One call**

```
10,069 tokens × $0.10 / 1,000,000 = $0.0010069
                                  ≈ $0.0010   (about one tenth of a cent)
```

**1,000 calls**

```
$0.0010069 × 1,000 = $1.0069
                   ≈ $1.01
```

---

## 4. Cost with cached tokens

With caching, the first call writes the handbook into the cache at the cache-write price. Every later call reads it back at the cached-input price.

**One call**

A single call can't benefit from a cache it is creating, so there are two cases:

```
First (cold) call — writes the cache:
10,069 tokens × $0.125 / 1,000,000 = $0.001258625   ≈ $0.0013

Any later (warm) call — cache hit:
10,069 tokens × $0.01  / 1,000,000 = $0.00010069    ≈ $0.0001
```

**1,000 calls** = 1 cache write + 999 cache hits

```
Cache write (call 1):     1 × $0.001258625  = $0.001258625
Cache hits (calls 2–1000): 999 × $0.00010069 = $0.100589310
                                              -------------
Total                                         = $0.101847935
                                              ≈ $0.10
```

---

## 5. Summary

| Scenario | One call | 1,000 calls |
|---|---:|---:|
| **Without caching** | $0.0010069 | **$1.0069** (≈ $1.01) |
| **With caching** | $0.0012586 (cold, writes cache) / $0.0001007 (warm, cache hit) | **$0.1018** (≈ $0.10) |

**Savings over 1,000 calls**

```
$1.0069000 − $0.1018479 = $0.9050521 saved
$0.9050521 ÷ $1.0069000 = 89.9% cheaper
```

- **One call:** caching costs slightly *more*. The cache write is $0.125/1M versus $0.10/1M uncached, so it costs $0.00025 extra.
- **Two calls or more:** caching already comes out ahead. Two calls cost $0.0013593 cached versus $0.0020138 uncached.
- **1,000 calls:** caching pays for itself many times over. It cuts the handbook cost by about 90%.

---

## 6. Assumptions

1. **Handbook only.** These numbers cover just the 10,069 handbook tokens. A real call also sends a system prompt, the vendor document and a few message-formatting tokens, and it pays $0.50/1M for output. Those costs come on top of this.
2. **Identical prefix.** Caching only works if the handbook is sent **byte-for-byte identical, at the start of the prompt**, on every call. Anything that changes per call, like the vendor document, has to come after it.
3. **Cache stays warm.** The 1,000-call figure assumes the calls run close enough together that the cache doesn't expire between them. If it expires, each refresh pays the cache-write price again.
4. **Tokenizer.** Luna's exact tokenizer isn't published in `tiktoken`, so `o200k_base` is the best available proxy. The usage report from a real API call (`usage.prompt_tokens`) would confirm the exact count.
5. **Cache granularity (side check).** OpenAI-style caches match prefixes in 128-token blocks after the first 1,024 tokens. If Luna works the same way, 9,984 of the 10,069 tokens would be cached and 85 would be billed at the full rate. That works out to $0.00010834 per warm call and $0.1095 per 1,000 calls. The conclusion doesn't change: caching saves about 89%.
