# import os
# import shutil
# from pathlib import Path
#
# def duplicate_files_in_folder(folder_path: str, total_copies: int = 4):
#     """
#     Duplicates every file in `folder_path` so that, in the end, each original file
#     appears `total_copies` times (including the original). New copies are named
#     with zero-padded indices, continuing from where the originals leave off.
#
#     Example (total_copies=4) for a folder with:
#       00000000.jpg
#       00000001.jpg
#       00000002.jpg
#
#     Result:
#       00000000.jpg    ← original
#       00000001.jpg    ← original
#       00000002.jpg    ← original
#       00000003.jpg    ← copy of 00000000.jpg
#       00000004.jpg    ← copy of 00000001.jpg
#       00000005.jpg    ← copy of 00000002.jpg
#       00000006.jpg    ← copy of 00000000.jpg
#       00000007.jpg    ← copy of 00000001.jpg
#       00000008.jpg    ← copy of 00000002.jpg
#       00000009.jpg    ← copy of 00000000.jpg
#       00000010.jpg    ← copy of 00000001.jpg
#       00000011.jpg    ← copy of 00000002.jpg
#
#     Args:
#         folder_path (str): Path to the directory containing the files to duplicate.
#         total_copies (int): How many times each original file should appear
#                              (including the original). Defaults to 4.
#     """
#     folder = Path(folder_path)
#     if not folder.is_dir():
#         raise ValueError(f"{folder_path!r} is not a valid directory.")
#
#     # 1) Gather all files in the folder and sort them by name.
#     #    We assume filenames are something like "00000000.jpg", "00000001.jpg", etc.
#     all_files = sorted([f for f in folder.iterdir() if f.is_file()])
#
#     if not all_files:
#         print("No files found in the specified folder.")
#         return
#
#     # 2) Determine the zero-padding length and extension from the first file.
#     #    E.g. if the first file is "00001234.jpg", then pad_length = 8, ext = ".jpg"
#     first_name = all_files[0].name  # e.g. "00000000.jpg"
#     name_stem, ext = os.path.splitext(first_name)
#     pad_length = len(name_stem)     # e.g. 8
#
#     # 3) Count how many original files there are.
#     n_orig = len(all_files)
#
#     # 4) How many new copies of the entire set we need?
#     #    If total_copies = 4, we need 3 additional sets (since originals count as 1).
#     n_additional_sets = total_copies - 1
#     if n_additional_sets <= 0:
#         print("total_copies must be at least 1.")
#         return
#
#     # 5) For each copy set i=1..n_additional_sets, copy all originals in order.
#     #    New index for file j in original list is: new_idx = j + i * n_orig
#     for i in range(1, n_additional_sets + 1):
#         for j, orig_path in enumerate(all_files):
#             new_idx = j + i * n_orig
#             new_name = f"{new_idx:0{pad_length}d}{ext}"
#             dst_path = folder / new_name
#
#             # Copying the file
#             shutil.copy2(orig_path, dst_path)
#
#     print(f"Duplicated {n_orig} original files into {n_additional_sets} additional sets "
#           f"(total {total_copies} copies each) in '{folder_path}'.")
#
#
# if __name__ == "__main__":
#     # Example usage:
#     #   python duplicate_files.py /path/to/my/folder 4
#     import sys
#
#     folder_arg = "/mnt/hdd/lab/datasets/freihand/freihand_orig/FreiHAND_pub_v2/training/mesh"
#     copies_arg = 4  # default to 4 total copies
#
#     duplicate_files_in_folder(folder_arg, total_copies=copies_arg)




# import json
#
# # 1) Read the original JSON (assumed to be a top‐level list).
# with open('/mnt/hdd/lab/datasets/freihand/freihand_orig/FreiHAND_pub_v2/training_xyz.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# # Ensure it really is a list
# if not isinstance(data, list):
#     raise ValueError("Expected top‐level JSON to be a list, but got %r" % type(data))
#
# # 2) Expand the list: original + 3 more copies
# expanded_list = data * 4
#
# # 3) Write the expanded list back to disk
# with open('/mnt/hdd/lab/datasets/freihand/freihand_orig/FreiHAND_pub_v2/training_xyz_e.json', 'w', encoding='utf-8') as f:
#     json.dump(expanded_list, f, indent=2)




# import json
#
# # 1) Load the original JSON (assumed to be a top‐level list)
# with open('/mnt/hdd/lab/datasets/freihand/freihand_orig/FreiHAND_pub_v2/training_xyz.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# # 2) Verify it’s a list, then drop the first 4000 entries
# if not isinstance(data, list):
#     raise ValueError(f"Expected top‐level JSON to be a list, but got {type(data)}")
# trimmed = data[4000:]
#
# # 3) Write the trimmed list back to disk (overwriting or into a new file)
# with open('/mnt/hdd/lab/datasets/freihand/freihand_orig/FreiHAND_pub_v2/training_xyz_e.json', 'w', encoding='utf-8') as f:
#     json.dump(trimmed, f, indent=2)



# import os
# from pathlib import Path
#
# def delete_first_n_files(folder_path: str, n: int = 4000, extension: str = ".jpg"):
#     """
#     Deletes the first `n` files in a zero-padded, sorted sequence from `00000000.ext` to
#     `0000{n-1:04d}.ext` (e.g. `00003999.jpg` if n=4000 and extension=".jpg").
#
#     Args:
#         folder_path (str): Path to the folder containing the files.
#         n (int, optional): Number of files to delete, starting from 0. Defaults to 4000.
#         extension (str, optional): File extension (including the dot). Defaults to ".jpg".
#     """
#     folder = Path(folder_path)
#
#     for i in range(n):
#         # Construct the zero-padded filename, e.g. "00000000.jpg"
#         filename = f"{i:08d}{extension}"
#         file_path = folder / filename
#
#         if file_path.exists():
#             try:
#                 file_path.unlink()  # delete the file
#                 print(f"Deleted: {file_path.name}")
#             except Exception as e:
#                 print(f"Error deleting {file_path.name}: {e}")
#         else:
#             print(f"Not found (skipping): {file_path.name}")
#
# if __name__ == "__main__":
#     # Example usage: replace with your actual folder path
#     target_folder = "/mnt/hdd/lab/datasets/freihand/freihand_orig/FreiHAND_pub_v2/training/mesh"
#     delete_first_n_files(target_folder, n=4000, extension=".ply")



# import os
# from pathlib import Path
#
# def rename_files_sequentially(folder_path: str, extension: str = ".jpg"):
#     """
#     Renames all files in `folder_path` with the given `extension` so that they
#     form a zero-padded, sequential index starting at 0.
#     E.g.:
#       "00004000.jpg" → "00000000.jpg"
#       "00004001.jpg" → "00000001.jpg"
#       ...
#     """
#
#     folder = Path(folder_path)
#     # 1) Gather all matching files and sort them by name
#     files = sorted(folder.glob(f"*{extension}"))
#
#     # 2) Rename each file to its new zero-padded index
#     for new_index, old_path in enumerate(files):
#         new_name = f"{new_index:08d}{extension}"
#         new_path = folder / new_name
#
#         try:
#             old_path.rename(new_path)
#             print(f"Renamed: {old_path.name} → {new_name}")
#         except Exception as e:
#             print(f"Error renaming {old_path.name}: {e}")
#
# if __name__ == "__main__":
#     # Example usage: replace with the actual path to your directory
#     target_folder = "/mnt/hdd/lab/datasets/freihand/freihand_orig/FreiHAND_pub_v2/training/mask"
#     rename_files_sequentially(target_folder, extension=".jpg")



import json

# 1) Load the original JSON (assumed to be a top-level list)
with open('/mnt/hdd/lab/datasets/freihand/freihand_orig/FreiHAND_pub_v2/training_xyz.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2) Verify it’s a list, then keep only the first 100 entries
if not isinstance(data, list):
    raise ValueError(f"Expected top-level JSON to be a list, but got {type(data)}")
trimmed = data[:100]

# 3) Write the trimmed list back to disk (overwriting or into a new file)
with open('/mnt/hdd/lab/datasets/freihand/freihand_orig/FreiHAND_pub_v2/training_xyz_e.json', 'w', encoding='utf-8') as f:
    json.dump(trimmed, f, indent=2)