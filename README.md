# Kettle

Reference implementation and cost model for the Kettle threshold signing
protocol, evaluated on HAWK-1024 parameters (`N = 1024`).

## Requirements

This README assumes MP-SPDZ is already installed and built. If it is not,
follow the [MP-SPDZ installation
guide](https://github.com/data61/MP-SPDZ?tab=readme-ov-file#installation)
first (also available in the
[documentation](https://mp-spdz.readthedocs.io/en/latest/readme.html#installation)).

`costs.py` needs nothing but Python 3.12 or newer.

## Running `kettle.mpc`

Copy the program into the MP-SPDZ source tree and run everything below from the
MP-SPDZ root:

```bash
cp kettle.mpc /path/to/MP-SPDZ/Programs/Source/
cd /path/to/MP-SPDZ
```

### 1. Compile

The field and ring domains need different bytecode:

```bash
./compile.py -F 64 kettle          # -> kettle       (the three field protocols)
./compile.py -R 64 kettle ring     # -> kettle-ring  (Fantastic Four)
```

### 2. Generate preprocessing (field protocols only)

The three field protocols are benchmarked with file preprocessing (`-F`), so
their timings measure the online phase. `-lgp` must be the same here and in
step 3, or the virtual machine will not find its data.

```bash
./Fake-Offline.x <n> -lgp 64 -p kettle             # MASCOT
./Fake-Offline.x <n> -T <t> -lgp 64 -p kettle      # both Shamir protocols
```

### 3. Run

All four protocols are maliciously secure and differ in the corruption model.

| Protocol | Command | Security model |
| --- | --- | --- |
| MASCOT | `PLAYERS=<n> Scripts/mascot.sh kettle -F -lgp 64` | Dishonest majority, up to `n-1` corruptions, field |
| Malicious Shamir | `PLAYERS=<n> THRESHOLD=<t> Scripts/mal-shamir.sh kettle -F -lgp 64` | Honest majority, `t < n/2`, field, Beaver triples |
| SPDZ-wise Shamir | `PLAYERS=<n> Scripts/sy-shamir.sh kettle -F -lgp 64 -T <t>` | Honest majority, `t < n/2`, field, no triples (MAC-checked) |
| Fantastic Four | `Scripts/rep4-ring.sh kettle-ring` | 4 parties, 1 corruption, ring `Z_{2^64}` |

Note that the two Shamir protocols receive the threshold differently:
`mal-shamir.sh` reads it from the environment, while `sy-shamir.sh` only
forwards `-T` on the command line. Fantastic Four is 4-party by construction
and takes neither argument (`rep4-ring.sh` hardcodes `PLAYERS=4`).

The reported benchmark uses `<n> = 8` parties and `<t> = 3`.

## Computing communication costs (`costs.py`)

`costs.py` is an analytic model of the protocol's communication: it reports
how many bytes each party sends in one signing execution, without running any
MPC. Run it directly:

```bash
python3 costs.py
```

The entry point is `compute_costs(ar_share_size, bo_share_size)`, taking the
size in bits of one arithmetic share and one boolean share. `N = 1024` matches `kettle.mpc`.
