STATE_5_PROPOSED_TRANSITION_MATRIX = (
    [0, 1, 0, 0, 0],
    [0, 0.6, 0.4, 0, 0],
    [0, 0, 0.6, 0.4, 0],
    [0, 0, 0, 0.7, 0.3],
    [0, 0, 0, 0, 0],
)


def matrix_to_float_string(matrix, indentation_number=9):
    returning_string = ""
    for row in matrix:
        returning_string += f'{" "*indentation_number}{" ".join([str(float(x)) for x in row])}\n'

    return returning_string


def generate_means_and_variances(states, vector_size, indentation_number=4):
    returning_string = ""
    for i in range(2, states):
        returning_string += f"""
{" "*indentation_number}<State> {i}
{" "*indentation_number}<Mean> {vector_size}
{" "*indentation_number}    {"0.0 "*vector_size}
{" "*indentation_number}<Variance> {vector_size}
{" "*indentation_number}    {"1.0 "*vector_size}"""

    return returning_string


def execute_script(
        output_file,
        vector_size=39,
        vector_type='MFCC_0_D_A',
        states=5,
        transition_matrix=STATE_5_PROPOSED_TRANSITION_MATRIX
):
    output_file = open(output_file, 'w+')
    output_file.write(f"""~o <VecSize> {vector_size} <{vector_type}>
~h "proto"
<BeginHMM>
    <NumStates> {states}{generate_means_and_variances(states, vector_size)}
    <TransP> {states}
{matrix_to_float_string(transition_matrix)}<EndHMM>
""")
