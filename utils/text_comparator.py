import difflib

def compare_texts(text1, text2):
    d = difflib.HtmlDiff()
    return d.make_table(
        text1.splitlines(), 
        text2.splitlines(), 
        fromdesc='Document 1', 
        todesc='Document 2',
        context=True,
        numlines=2
    )

