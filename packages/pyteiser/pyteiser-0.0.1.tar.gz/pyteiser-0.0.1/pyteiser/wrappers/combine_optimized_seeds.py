import numpy as np
import argparse
import math

import os

from .. import IO


def handler():
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimized_seeds_folder", help="optimized seeds", type=str)
    parser.add_argument("--optimized_profiles_folder", help="profiles of optimized seeds", type=str)
    parser.add_argument("--optimized_MI_pv_zscores_folder", help="MI values, p-values and z-scores", type=str)
    parser.add_argument("--robustness_array_folder", help="vector indicating which seeds have passed the robustness test", type=str)

    parser.add_argument("--optimized_seeds_filename_template", help="", type=str)
    parser.add_argument("--optimized_profiles_filename_template", help="", type=str)
    parser.add_argument("--optimized_MI_pv_zscores_filename_template", help="", type=str)
    parser.add_argument("--robustness_array_filename_template", help="", type=str)

    parser.add_argument("--combined_seeds_filename", help="output: ", type=str)
    parser.add_argument("--combined_profiles_filename", help="output: ", type=str)
    parser.add_argument("--combined_MI_pv_zscores_filename", help="output: ", type=str)
    parser.add_argument("--combined_robustness_filename", help="output: ", type=str)

    parser.add_argument("--indices_mode", help="compression in the index mode", type=bool)
    parser.add_argument("--index_bit_width", help="number of bits per one index when compressing", type=int)

    parser.set_defaults(
        indices_mode=False,
        index_bit_width = 24,
    )

    args = parser.parse_args()

    return args


def get_list_files(args):
    filenames_tuples_list = []

    indices_list_int = []
    short_fns_list = os.listdir(args.optimized_seeds_folder)

    for short_fn in short_fns_list:
        if not short_fn.endswith('.bin'):
            continue
        split_array = short_fn.replace('.bin','').split('_')
        current_template = "_".join(split_array[:-1])
        # make sure to only include files from the same run/filename template
        if current_template != args.optimized_seeds_filename_template:
            continue
        index = int(split_array[-1])
        indices_list_int.append(index)

    indices_list_int_sorted = sorted(indices_list_int)
    indices_list_str = [str(x) for x in indices_list_int_sorted]

    for i in indices_list_str:
            seed_filename_short = "%s_%s.bin" % (args.optimized_seeds_filename_template, i)
            profiles_filename_short = "%s_%s.bin" % (args.optimized_profiles_filename_template, i)
            char_filename_short = "%s_%s.bin" % (args.optimized_MI_pv_zscores_filename_template, i)
            robustness_filename_short = "%s_%s.bin" % (args.robustness_array_filename_template, i)

            seeds_filename_full = os.path.join(args.optimized_seeds_folder, seed_filename_short)
            profiles_filename_full = os.path.join(args.optimized_profiles_folder, profiles_filename_short)
            char_filename_full = os.path.join(args.optimized_MI_pv_zscores_folder, char_filename_short)
            robustness_filename_full = os.path.join(args.robustness_array_folder, robustness_filename_short)

            tuple_filenames = (seeds_filename_full, profiles_filename_full,
                                char_filename_full, robustness_filename_full)
            filenames_tuples_list.append(tuple_filenames)

    return filenames_tuples_list


def read_chunks(filenames_tuples_list, indices_mode):
    seeds_optimized_list = []
    profiles_optimized_gen_list = []
    seed_charact_gen_list = []
    robustness_gen_list = []

    for tup in filenames_tuples_list:
        seeds_filename_full, profiles_filename_full, \
        char_filename_full, robustness_filename_full = tup

        seeds_optimized = IO.read_motif_file(seeds_filename_full)
        profiles_optimized = IO.unpack_profiles_file(profiles_filename_full, indices_mode)
        seed_charact_curr = IO.read_np_array(char_filename_full, np.dtype('float64'))
        robustness_curr_array = IO.read_np_array(robustness_filename_full, np.dtype('bool'))
        robustness_curr_list = list(robustness_curr_array)

        seeds_optimized_list += seeds_optimized
        profiles_optimized_gen_list.append(profiles_optimized)
        seed_charact_gen_list.append(seed_charact_curr)
        robustness_gen_list += robustness_curr_list

    profiles_optimized_array = np.concatenate(profiles_optimized_gen_list, axis=0)
    seed_charact_array = np.concatenate(seed_charact_gen_list, axis=0)
    robustness_array = np.array(robustness_gen_list, dtype=bool)

    return seeds_optimized_list, profiles_optimized_array, seed_charact_array, robustness_array


def main():
    args = handler()

    filenames_tuples_list = get_list_files(args)

    seeds_optimized_list, profiles_optimized_array, \
    seed_charact_array, robustness_array = read_chunks(filenames_tuples_list, args.indices_mode)


    IO.write_list_of_seeds(seeds_optimized_list, args.combined_seeds_filename)
    IO.write_array_of_profiles(profiles_optimized_array, args.combined_profiles_filename,
                               args.indices_mode, args.index_bit_width)
    IO.write_np_array(seed_charact_array, args.combined_MI_pv_zscores_filename)
    IO.write_np_array(robustness_array, args.combined_robustness_filename)





if __name__ == "__main__":
    main()













