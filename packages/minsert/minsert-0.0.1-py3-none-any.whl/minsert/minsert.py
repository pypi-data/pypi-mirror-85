import logging
import os


def is_comment(line: str) -> bool:
    ln = line.strip()
    if ln.startswith('<!--') and ln.endswith('-->'):
        return True
    return False


def is_starter(line: str) -> str or None:
    if is_comment(line):
        try:
            get1 = line.split('➡️')[-1].strip()
            return get1.split('⬅️')[0].strip()
        except Exception as err:
            logging.warning(err)


def is_ender(line: str) -> bool:
    if is_comment(line):
        return '🛑' in line


class MarkdownFile():
    def __init__(self, file_path: str) -> None:
        if os.path.isfile(file_path) and file_path.endswith('.md'):
            self.file_path = file_path
        else:
            raise FileNotFoundError('the path you gave is invalid')

    def insert(self, things):

        new_lines = []
        with open(self.file_path) as file:
            lines = file.readlines()

        inside_a_block = False
        count = 0

        for line in lines:
            if not inside_a_block:
                new_lines.append(line)
                count += 1
                start_of = is_starter(line)
                if not start_of:
                    continue
                else:
                    try:
                        content = things[start_of].split('\n')
                        count += len(content)
                    except KeyError:
                        logging.warning(
                            f'\t "{start_of}" in line {count} of {self.file_path} not found.')
                        content = ''
                    content = [ln+'\n' for ln in content]
                    new_lines += content
                    inside_a_block = True
            elif is_ender(line):
                new_lines.append(line)
                count += 1
                inside_a_block = False
            else:
                continue

        if inside_a_block:
            raise ValueError('block not closed')

        with open(self.file_path, 'w') as file:
            file.writelines(new_lines)
