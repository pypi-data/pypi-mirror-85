# MIT License
#
# Copyright (c) 2018 Olaf Haag
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" Convert animation data in BVH files to CSV format.
Rotation data and position are separate output files.
The first line is a header with each degree of freedom as a column.
The first column is the frame for the data in that row.
The second column is the time of the frame in seconds.
The degrees of freedom in the joints are written in the order they appear in the BVH file as channels.
"""

import os
import sys
import argparse
from multiprocess import Pool, freeze_support
from functools import partial
import time
import glob

from . import bvh2csv


def bvh2csv_batch(bvh_files,
                  dst_dirpath=None,
                  scale=1.0,
                  export_rotation=True,
                  export_position=True,
                  export_hierarchy=False,
                  end_sites=True):
    """Convert BVH files to CSV table format."""
    print("Converting {} files...".format(len(bvh_files)))
    n_processes = min(len(bvh_files), 8)
    print("\nCreating pool with {} processes".format(n_processes))
    with Pool(processes=n_processes) as p:
        res = p.map(partial(bvh2csv,
                            dst_dirpath=dst_dirpath,
                            scale=scale,
                            export_rotation=export_rotation,
                            export_position=export_position,
                            export_hierarchy=export_hierarchy,
                            end_sites=end_sites),
                    bvh_files)
    # Were there errors?
    num_errors = len(res) - sum(res)
    if num_errors > 0:
        print("ERROR: {} conversions were not successful.".format(num_errors))
    return num_errors


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog=__file__,
        description="""Convert BVH files to CSV table format.""",
        epilog="""If neither -p nor -r are specified, both rotation and position CSV files will be created for each BVH file.""",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-v", "--ver", action='version', version='%(prog)s 0.1')
    parser.add_argument("-o", "--out", type=str, default='',
                        help="Destination folder for CSV files.\n"
                             "If no destination path is given, BVH file path is used.\n"
                             "CSV files will have the source file base name appended by\n"
                             "suffixes _rot, _pos, and _hierarchy.csv respectively.")
    parser.add_argument("-s", "--scale", type=float, default=1.0,
                        help="Scale factor for root position and offset values.\n"
                             "In case you have to switch from centimeters to meters or vice versa.")
    parser.add_argument("-r", "--rotation", action='store_true', help="Output rotation CSV files.")
    parser.add_argument("-p", "--position", action='store_true', help="Output world space position CSV files.")
    parser.add_argument("-H", "--hierarchy", action='store_true', help="Output skeleton hierarchy to CSV file.")
    parser.add_argument("-e", "--ends", action='store_true', help="Include BVH End Sites in position CSV. "
                                                                  "They do not have rotations.")
    parser.add_argument("input folder", type=str, help="Folder containing BVH source files.")
    args = vars(parser.parse_args(argv))
    src_folder_path = args['input folder']
    dst_folder_path = args['out']
    scale_factor = args['scale']
    do_rotation = args['rotation']
    do_position = args['position']
    # If neither rotation nor position are specified, do both.
    if not do_rotation and not do_position:
        do_rotation = True
        do_position = True
    do_hierarchy = args['hierarchy']
    do_end_sites = args['ends']
    
    if not os.path.exists(src_folder_path):
        print("ERROR: Folder not found", src_folder_path)
        return False
    
    os.chdir(src_folder_path)
    # Keep track of when we started.
    t0 = time.time()
    # Collect all BVH files in folder and pair with out file as arguments for converter.
    file_names = glob.glob("*.bvh")
    n_err = bvh2csv_batch(file_names,
                          dst_dirpath=dst_folder_path,
                          scale=scale_factor,
                          export_rotation=do_rotation,
                          export_position=do_position,
                          export_hierarchy=do_hierarchy,
                          end_sites=do_end_sites)
    print("Processing took: {:.2f} seconds".format(time.time() - t0))
    return False if n_err else True


if __name__ == "__main__":
    freeze_support()
    exit_code = int(not main())
    sys.exit(exit_code)
