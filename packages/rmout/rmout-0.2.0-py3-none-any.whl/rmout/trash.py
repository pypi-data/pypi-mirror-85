import os
from send2trash import send2trash


def extract_target_from_userinput() -> list:
    # input()からユーザー入力を取得し，ゴミ箱送り対象のコードリストを作成

    codes_string = input('send to trash [a] ? ')
    codes_string = codes_string.strip()  # .strip(',')
    codelist = codes_string.split(',')
    if len(set(codelist)) != len(codelist):
        try:
            raise ValueError('The input code may be duplicated.')
        except ValueError as e:
            print(f'{e} {codelist}')
            return list()
    codelist = [code.strip().lower() for code in codelist]
    return codelist


def get_extensiondir_for_sendtotrash(codelist, throwaway) -> list:
    # ゴミ箱送りの拡張子辞書を取得

    if 'a' in codelist or '' in codelist:
        pass
    elif 'x' in codelist:
        return list()
    else:
        # 不正な入力の処理
        ext_code_list = [str(target['extension_code'])
                         for target in throwaway]
        invalid_codes = [code for code in codelist
                         if not code in ext_code_list]
        if invalid_codes:
            try:
                raise ValueError('The input code is invalid.')
            except ValueError as e:
                print(f'{e} {invalid_codes}')
                return list()

        # ユーザー入力と一致した拡張子ファイルを抽出
        renew_throwaway = [target for target in throwaway
                           if str(target['extension_code']) in codelist]
        throwaway = renew_throwaway
    return throwaway


def send_to_trash(throwaway, debug=False) -> None:
    # 削除対象のファイルをゴミ箱へ送る

    if throwaway:
        for target in throwaway:
            for target_file_path in target['file_path']:
                if debug:
                    print(os.path.basename(target_file_path))
                else:
                    print(os.path.basename(target_file_path))
                    send2trash(str(target_file_path))
