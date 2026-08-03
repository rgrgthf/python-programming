def word_len(text):
    count = {}
    for w in text.split():
        count[w] = len(w)
    return count
#我不知道是不是这样写
s = "the quick brown fox jumps over the lazy dog the fox"
word_len(s)
print(word_len(s))