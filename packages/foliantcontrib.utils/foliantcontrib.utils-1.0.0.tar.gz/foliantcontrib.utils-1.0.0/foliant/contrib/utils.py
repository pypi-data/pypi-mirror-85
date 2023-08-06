from pathlib import PosixPath


def prepend_file(
    filepath: str or PosixPath,
    content: str,
    before_yfm=False,
    before_heading=True
):
    '''
    Insert `content` at the beginning of the file `filepath`.

    :param filepath: path to file which needs to be prepended.
    :param content: content to be inserted.
    :before_yfm: if file starts with YAML Front Matter, insert content before it
    :before_yfm: if file starts with a heading, insert content before it
    '''
    with open(filepath, encoding='utf8') as f:
        source = f.read()

    start = 0

    if not before_yfm and source.startswith('---\n'):
        yfm_end = source.find('\n---\n', 1)
        start = yfm_end + len('\n---\n') if yfm_end != -1 else 0
    if not before_heading and source.startswith('#'):
        start = source.find('\n', 1) + 1
        if start == 0:
            start = len(source)
        # add a line break just in case for not to break thea heading
        content = '\n' + content

    processed_content = source[:start] + content + source[start:]

    with open(filepath, 'w', encoding='utf8') as f:
        f.write(processed_content)
