def write_boolean(boolean):
    return 'T' if boolean else 'F'


def execute_script(
        output_file,
        source_format='WAV',
        target_kind='MFCC_0',
        target_rate=100000.0,
        save_compressed=True,
        save_with_rc=True,
        window_size=250000.0,
        use_hamming=True,
        pre_em_coef=0.97,
        num_chans=26,
        cep_lifter=22,
        num_ceps=12,
        e_normalise=False
):
    output_file = open(output_file, 'w+')
    output_file.write(
f"""SOURCEFORMAT = {source_format}
TARGETKIND = {target_kind}
TARGETRATE = {target_rate}
SAVECOMPRESSED = {write_boolean(save_compressed)}
SAVEWITHRC = {write_boolean(save_with_rc)}
WINDOWSIZE = {window_size}
USEHAMMING = {write_boolean(use_hamming)}
PREEMCOEF = {pre_em_coef}
NUMCHANS = {num_chans}
CEPLIFTER = {cep_lifter}
NUMCEPS = {num_ceps}
ENORMALISE = {write_boolean(e_normalise)}
""")
    output_file.close()
