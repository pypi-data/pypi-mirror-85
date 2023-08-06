
def apply_agesex_edits(cc_dct, age, sex):
    # age/sex edits. see "V22I0ED2.TXT"
    elst0 = ["D66", "D67"]
    elst1 = ["J410", "J411", "J418", "J42", "J430", "J431", "J432", 
            "J438", "J439", "J440", "J441", "J449", "J982", "J983"]
    elst2 = ["F3481"]
    if sex == "F":
        for dx in (dx for dx in elst0 if dx in cc_dct):
            cc_dct[dx] = "HCC48" 
    if age < 18:
        for dx in (dx for dx in elst1 if dx in cc_dct):
            cc_dct[dx] = "HCC112"
    if age < 6 or age > 18:
        for dx in (dx for dx in elst2 if dx in cc_dct):
            cc_dct[dx] = "HCCNA"
    cc_dct = {dx:cc for dx, cc in cc_dct.items() if cc != "HCCNA"}
    return cc_dct

