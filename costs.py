"""Per-party communication costs for the Kettle threshold signature protocol.

Estimates the offline and online communication footprint, per signature and
per party, of the two protocol variants:

  RO (round-optimized, PSign):           quadratic offline precomputation,
                                         2 online rounds;
  CO (communication-optimized, PCOSign): linear offline phase,
                                         3 online rounds.

Cost model (honest-majority Shamir sharing):
  - an arithmetic share is k = ceil(log2 q) bits and a Boolean share is
    kappa bits, where F_{2^kappa} supports up to 2^kappa - 1 parties;
  - opening one shared value costs one share sent per party;
  - a multiplication (Beaver) costs two openings, i.e. two shares per party;
  - the generation of correlated randomness (daBits, Beaver triples) is
    excluded, as are the negligible 2n Hadamard products r (.) Dx
    (2*n*2*k bits per party).

The Gaussian sampler follows the Hawk RCDTs: 13 table entries at 78-bit
precision per half-Gaussian, identical for Hawk-512 and Hawk-1024.
"""


def compute_costs(ar_share_size, bo_share_size, n=512):
    kb = 8000
    nbfmt = " >10.2f"
    strfmt = " >40"
    max_users = 2 ** bo_share_size - 1
    print(f"Assuming: n = {n} (at most {max_users} users)")
    print(f"{'1 Arithmetic share costs':{strfmt}} {ar_share_size: >10}b")
    print(f"{'1 Boolean share costs':{strfmt}} {bo_share_size: >10}b")
    print()

    # 4n half-Gaussian samples per signature: 2n coordinates times 2 cosets.
    common = n * 2 * 2

    # 13 leq gates per sample, each ~2*78 Boolean multiplications
    # (Brent-Kung), at 2*kappa bits per multiplication per party.
    secleq_s = common * 78 * (2 * 2) * 13 * bo_share_size / kb
    print(f"{'Secleq com.cost/party:':{strfmt}} {secleq_s:{nbfmt}}kB")

    # 13 daBit mask openings per sample, in the Boolean domain.
    dabits_s = common * 13 * bo_share_size / kb
    print(f"{'Dabits opening com.cost/party:':{strfmt}} {dabits_s:{nbfmt}}kB")

    # One arithmetic multiplication per sample to apply the Gaussian sign.
    sign_s = common * 2 * ar_share_size / kb
    print(f"{'Sign computation com.cost/party:':{strfmt}} {sign_s:{nbfmt}}kB")

    # Linearization (RO only): 4n^2 arithmetic multiplications, namely the
    # n x 2n matrix V (2n^2 products) and w0 = M.s0 (two ring products,
    # 2n^2 schoolbook products).
    precompute_mul_s = common * 2 * n * ar_share_size / kb
    print(f"{'Precomputed muls (RO only):':{strfmt}} {precompute_mul_s:{nbfmt}}kB")

    # Opening of w1: n arithmetic shares.
    online_sig_open_s = n * ar_share_size / kb
    print(f"{'Signature opening (online):':{strfmt}} {online_sig_open_s:{nbfmt}}kB")

    # CO only: two ring products with fixed secret operands (f and g), each
    # opening one masked n-coefficient vector.
    online_poly_mul_s = n * 2 * ar_share_size / kb
    print(f"{'Polynomial multiplication (online, CO):':{strfmt}} {online_poly_mul_s:{nbfmt}}kB")

    # Round-1 opening of the masked coset vector c in F_2^{2n}, one Boolean
    # share per coefficient. Reported separately; excluded from the totals.
    c_open_s = 2 * n * bo_share_size / kb
    print(f"{'c-opening (online, excl. from totals):':{strfmt}} {c_open_s:{nbfmt}}kB")

    mb = 1000
    total_ro = (secleq_s + dabits_s + sign_s + precompute_mul_s) / mb
    total_co = (secleq_s + dabits_s + sign_s) / mb
    online_cost_ro = online_sig_open_s
    online_cost_co = online_sig_open_s + online_poly_mul_s
    print(f"{'Offline cost RO:':{strfmt}} {total_ro:{nbfmt}}MB")
    print(f"{'Online cost RO:':{strfmt}} {online_cost_ro:{nbfmt}}kB")
    print(f"{'Offline cost CO:':{strfmt}} {total_co:{nbfmt}}MB")
    print(f"{'Online cost CO:':{strfmt}} {online_cost_co:{nbfmt}}kB")

    print(f"{'Total memory footprint RO:':{strfmt}} {max_users * total_ro:{nbfmt}}MB")
    print(f"{'Total memory footprint CO:':{strfmt}} {max_users * total_co:{nbfmt}}MB")
    print()


compute_costs(15, 10, n=512)     # Hawk-512
compute_costs(15, 10, n=1024)    # Hawk-1024
# compute_costs(15, 11, n=1024)  # kappa = 11: supports up to 2047 parties
