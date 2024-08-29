import multiprocessing
import itertools

def run(args):
    query, cursor, cursor2 = args
    print( query, cursor, cursor2)

queries = ["foo", "bar", "blub"]
cursor = ["whatever", "22"]
cursor2 = ["111", "2333"]

if __name__ == '__main__':
    with multiprocessing.Pool(processes=10) as pool:
        allPossible = [x for x in itertools.product(queries, cursor, cursor2)]
        results = pool.map(run, allPossible)

    print(results)

print(list(range(1,100)))

