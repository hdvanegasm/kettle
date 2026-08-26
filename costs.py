def compute_costs(ar_share_size, bo_share_size):
    kb = 8092
    n = 512
    nbfmt = " >10.2f"
    strfmt = " >40"
    max_users = 2 ** bo_share_size
    print(f"Assuming: (at most {max_users} users)")
    print(f"{"1 Arithmetic share costs":{strfmt}} {ar_share_size: >10}b")
    print(f"{"1 Boolean share costs":{strfmt}} {bo_share_size: >10}b")
    print()

    common = n * 2 * 2 # n * nb_keys * nb_centers
    secleq_s = common * 78 * ( 2 * 2 ) * 13 * bo_share_size / kb
    print(f"{"Secleq com.cost/party:":{strfmt}} {secleq_s:{nbfmt}}kB")

    dabits_s = common * 13 * bo_share_size /kb
    print(f"{"Dabits opening com.cost/party:":{strfmt}} {dabits_s:{nbfmt}}kB")

    sign_s = common * 2 * ar_share_size / kb
    print(f"{"Sign computation com.cost/party:":{strfmt}} {sign_s:{nbfmt}}kB")

    precompute_mul_s = common * 2 * n * ar_share_size / kb
    print(f"{"Precomputed muls (RO only):":{strfmt}} {precompute_mul_s:{nbfmt}}kB")

    mb = 1000
    gb = 1000
    total_ro = (secleq_s + dabits_s + sign_s + precompute_mul_s) / mb
    total_co = (secleq_s + dabits_s + sign_s) / mb
    print(f"{"Total size RO:":{strfmt}} {total_ro:{nbfmt}}MB")
    print(f"{"Total size CO:":{strfmt}} {total_co:{nbfmt}}MB")
    print(f"{"Total memory footprint RO:":{strfmt}} {max_users * total_ro:{nbfmt}}MB")
    print(f"{"Total memory footprint CO:":{strfmt}} {max_users * total_co:{nbfmt}}MB")

compute_costs(15, 10)
