import re
from collections import Counter

path = "/mnt/user-data/uploads/SQL_Full__Course_for_Beginners.txt"
with open(path, encoding="utf-8") as f:
    text = f.read()
text_flat = re.sub(r'\s+', ' ', text).strip()
word_pattern = re.compile(r"[A-Za-z']+")
words = [w.strip("'").lower() for w in word_pattern.findall(text_flat) if w.strip("'")]
freq = Counter(words)

basic = set("""a an the and or but if then so because as of at by for with about
against between into through during before after above below to from up down in out on off
over under again further once here there when where why how all any both each few more most
other some such no nor not only own same than too very s t can will just don should now i me
my myself we our ours ourselves you your yours yourself yourselves he him his himself she her
hers herself it its itself they them their theirs themselves what which who whom this that these
those am is are was were be been being have has had having do does did doing would could
ll re ve d m going go get got make made take taken want need know think see say said
also good well right okay ok yeah yes no thing things one two three first second
let's we're it's that's don't i'm you're going""".split())

filtered = [(w,c) for w,c in freq.most_common(600) if w not in basic and len(w) > 2]
for w,c in filtered[:220]:
    print(w, c)
