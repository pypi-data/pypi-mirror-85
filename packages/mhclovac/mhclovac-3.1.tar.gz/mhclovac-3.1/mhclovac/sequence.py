from proteinko import model_distribution


def validate_sequence(sequence: str, sequence_name: str, silent: bool = True) -> bool:
    """
    Checks if sequence contains only valid amino acid letter codes.

    :param sequence: Amino acid sequence in capital letters
    :param silent: Raises exception if False
    :return: bool, Exception
    """
    valid = ['C', 'D', 'S', 'Q', 'K', 'I', 'P', 'T', 'F', 'N', 'G', 'H', 'L', 'R', 'W', 'A', 'V', 'E', 'Y', 'M']
    for i, s in enumerate(sequence):
        if s not in valid:
            if not silent:
                msg = f'"{sequence_name}": amino acid "{s}" at position {i} is not valid.'
                raise ValueError(msg)
            return False
    return True


def chop_sequence(sequence: str, peptide_length: int) -> list:
    """
    Chops sequence into N fragments of peptide_length.

    :param sequence: Amino acid sequence
    :param peptide_length: Length of fragments
    :return: list
    """
    if len(sequence) < peptide_length:
        raise ValueError(f'sequence is shorter than peptide_length')
    fragments = []
    for i in range(len(sequence) - peptide_length + 1):
        peptide = sequence[i: i+peptide_length]
        fragments.append(peptide)
    return fragments


def read_fasta(fpath: str) -> (str, str):
    """
    Generator that reads fasta file and yields sequence name and sequence.

    :param fasta_path: string, path to fasta file
    :return: None
    """
    with open(fpath, 'r') as f:
        seq_name = ''
        sequence = ''
        write_flag = 0
        for line in f:
            if line.startswith('>'):
                if write_flag:
                    write_flag = 0
                    yield seq_name, sequence
                seq_name = line[1:].strip()
                sequence = ''
            else:
                sequence += line.strip()
                write_flag = 1
        yield seq_name, sequence


def sequence_to_features(sequence: str, index_list: list, sigma: float = 0.4, sampling_points: int = 9) -> list:
    """
    Converts sequence into feature array.

    :param sequence: Amino acid sequence
    :param index_list: List of python dicts
    :param sigma: Sigma factor used for modeling
    :param sampling_points: Length of single index array
    :return: Feature array of length len(index_list) * sampling_points
    """
    sequence_features = []
    for index in index_list:
        features = model_distribution(sequence, index, sigma=sigma, sampling_points=sampling_points)
        sequence_features.extend(features)
    return sequence_features
