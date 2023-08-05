import numpy as np
import argparse
import os

from .. import IO
from .. import matchmaker
from .. import type_conversions
from .. import sge

def handler():
    parser = argparse.ArgumentParser()

    parser.add_argument("--task_mapping_file", help="", type=str)

    parser.add_argument("--seed_folder", help="", type=str)
    parser.add_argument("--rna_bin_file", help="", type=str)
    parser.add_argument("--out_folder", help="", type=str)
    parser.add_argument("--inp_filename_template", help="", type=str)
    parser.add_argument("--out_filename_template", help="", type=str)
    parser.add_argument("--print_qstat", help="", type=str)
    parser.add_argument("--path_to_qstat", help="", type=str)
    parser.add_argument("--are_seeds_degenerate", help="", type=str)
    parser.add_argument("--indices_mode", help="compression in the index mode", type=bool)
    parser.add_argument("--index_bit_width", help="number of bits per one index when compressing", type=int)



    parser.set_defaults(

        # seed_folder='/wynton/home/goodarzi/khorms/pyteiser_root/testing_data/test_seeds',
        # out_folder='/wynton/home/goodarzi/khorms/pyteiser_root/testing_data/test_profiles',
        # inp_filename_template='test_seeds_101',
        # out_filename_template='test_motifs_101',
        seed_folder='/wynton/home/goodarzi/khorms/pyteiser_root/data/seeds/seeds_4-7_4-9_4-6_14-20/motifs_per_file_30k',
        out_folder='/wynton/home/goodarzi/khorms/pyteiser_root/data/profiles/profiles_4-7_4-9_4-6_14-20/profiles_per_file_30k',
        inp_filename_template='seeds_4-7_4-9_4-6_14-20_30k',
        out_filename_template='profiles_4-7_4-9_4-6_14-20_30k',
        rna_bin_file='/wynton/home/goodarzi/khorms/pyteiser_root/data/reference_transcriptomes/binarized/Gencode_v28_GTEx_expressed_transcripts_from_coding_genes_3_utrs_fasta.bin',
        path_to_qstat='/opt/sge/bin/lx-amd64/qstat',
        print_qstat='y',
        are_seeds_degenerate='n',
        indices_mode=False,
        index_bit_width = 24,

    )

    args = parser.parse_args()

    return args


def get_current_in_out_filenames(args, env_variables_dict, mapping_dict):
    file_index_to_use =  mapping_dict[env_variables_dict["task_id"]]
    inp_filename_short = "%s_%s.bin" % (args.inp_filename_template, file_index_to_use)
    out_filename_short = "%s_%s.bin" % (args.out_filename_template, file_index_to_use)
    seeds_filename_full = os.path.join(args.seed_folder, inp_filename_short)
    profiles_filename_full = os.path.join(args.out_folder, out_filename_short)
    rna_bin_filename = args.rna_bin_file

    return seeds_filename_full, profiles_filename_full, rna_bin_filename



def calculate_write_profiles(n_motifs_list, n_seqs_list,
                            out_filename, are_seeds_degenerate,
                            indices_mode, index_bit_width,
                             do_print=False, do_return = False):
    if are_seeds_degenerate == 'yes' or are_seeds_degenerate == 'y':
        is_degenerate = True
    else:
        is_degenerate = False

    with open(out_filename, 'wb') as wf:
        if do_return:
            profiles_list = [0] * len(n_motifs_list)

        for i, motif in enumerate(n_motifs_list):
            current_profile, time_spent = matchmaker.calculate_profile_one_motif(motif, n_seqs_list,
                                                                                 is_degenerate = is_degenerate)
            if indices_mode:
                current_profile.compress_indices(width = index_bit_width)
                wf.write(current_profile.bytestring_indices)
            else:
                current_profile.compress()
                wf.write(current_profile.bytestring)


            if do_return:
                profiles_list[i] = current_profile.values

            if do_print:
                print("Motif number %d binds %d sequences. It took %.2f seconds"
                      % (i, current_profile.sum(), time_spent))
    if do_return:
        profiles_array = np.array(profiles_list)
        return profiles_array


def read_input_files(seeds_filename_full, rna_bin_filename):
    seqs_dict, seqs_order = IO.read_rna_bin_file(rna_bin_filename)
    w_motifs_list = IO.read_motif_file(seeds_filename_full)
    w_seqs_list = [seqs_dict[name] for name in seqs_order]
    n_motifs_list = type_conversions.w_to_n_motifs_list(w_motifs_list)
    n_seqs_list = type_conversions.w_to_n_sequences_list(w_seqs_list)

    return n_motifs_list, n_seqs_list


def non_sge_dependent_main(seeds_filename_full, profiles_filename_full, rna_bin_filename,
                           are_seeds_degenerate,
                           indices_mode,
                           index_bit_width
                           ):
    # get the names of input and output files

    n_motifs_list, n_seqs_list = read_input_files(seeds_filename_full, rna_bin_filename)

    # the main procedure - calculate profiles
    calculate_write_profiles(n_motifs_list, n_seqs_list,
                             profiles_filename_full,
                             are_seeds_degenerate,
                             indices_mode,
                             index_bit_width,
                             do_print=True)



def main():
    args = handler()

    # get mapping of task ids to input files
    mapping_dict = sge.parse_task_mapping_file(args.task_mapping_file)

    # get the task id
    env_variables_dict = sge.get_env_variables()

    # get the input filenames
    seeds_filename_full, profiles_filename_full, rna_bin_filename = get_current_in_out_filenames(args,
                                                                                                 env_variables_dict,
                                                                                                 mapping_dict)

    # run the calculation
    non_sge_dependent_main(seeds_filename_full, profiles_filename_full, rna_bin_filename,
                           args.are_seeds_degenerate,
                           args.indices_mode,
                           args.index_bit_width,
                           do_print=True
                           )

    if args.print_qstat == 'y':
        sge.print_qstat_proc(env_variables_dict, args.path_to_qstat)


if __name__ == "__main__":
    main()


