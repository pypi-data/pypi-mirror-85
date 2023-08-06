import os
import pathlib


def get_extensions_set(current_dir) -> set:
    # ゴミ箱送りファイルの拡張子リストを取得

    EXTENSION_FILE = '.rmoutrc'
    home_dir = pathlib.Path.home()
    extfile_in_curr = os.path.join(current_dir, EXTENSION_FILE)
    extfile_in_home = os.path.join(home_dir, EXTENSION_FILE)

    target_ext_list = []
    if os.path.isfile(extfile_in_home):
        with open(extfile_in_home, 'r') as f:
            target_ext_list += [e.strip() for e in f.readlines() if e.strip()]
    if os.path.isfile(extfile_in_curr):
        with open(extfile_in_curr, 'r') as f:
            target_ext_list += [e.strip() for e in f.readlines() if e.strip()]
    if target_ext_set := set(target_ext_list):
        return target_ext_set
    else:
        print('The file to be deleted cannot be found.')
        return set()


def _std_out(throwaway) -> None:
    for target in throwaway:
        print(
            f'{target["extension_code"]:6}: {target["extension"]}  {len(target["file_path"])}')
    print(f'{"":5}a: all files')
    print(f'{"":5}x: exit')


def extract_files_by_extlist(target_ext_set, current_dir) -> list:
    # カレントディレクトリから拡張子リストに対応したファイルを抽出

    throwaway = []
    target_extension_code = 0
    for extension in sorted(target_ext_set):
        target_extension = '*' + extension
        target_files = pathlib.Path(current_dir).glob(target_extension)
        target_files = [f for f in target_files
                        if os.path.isfile(os.path.join(current_dir, f))]
        if target_files:
            target_extension_code += 1
            throwaway.append({
                'extension_code': target_extension_code,
                'extension': target_extension,
                'file_path': target_files,
            })
    if throwaway:
        _std_out(throwaway)
        return throwaway
    else:
        print('The file to be deleted cannot be found.')
        return list()
