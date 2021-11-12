import numpy as np
import faiss
import datetime
import argparse
import os


def time_str(microseconds):
    return "%f microsecs, %f millisecs, %f secsc" % (microseconds, microseconds / 1000, microseconds / 1000000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # dimension
    parser.add_argument('--d', type=int, default=2048)
    parser.add_argument('--topk', type=int, default=4)
    # database size
    parser.add_argument('--nb', type=int, default=200000)
    # nb of queries
    parser.add_argument('--nq', type=int, default=10000)

    args = parser.parse_args()

    np.random.seed(1234)  # make reproducible

    d = args.d
    topk = args.topk
    nb = args.nb
    nq = args.nq

    print("Dimension: %d" % (d))
    print("Records: %d" % (nb))
    print("Queries: %d" % (nq))
    print("Topk: %d" % (topk))

    start = datetime.datetime.now()
    print("### Start generating random data")

    xb = np.random.random((nb, d)).astype('float32')
    xb[:, 0] += np.arange(nb) / 1000.
    xq = np.random.random((nq, d)).astype('float32')
    xq[:, 0] += np.arange(nq) / 1000.

    end = datetime.datetime.now()

    generate_data_time = (end - start).microseconds

    print("### Generating random data costs %s" % (time_str(generate_data_time)))

    print("### Start to build index")

    start = datetime.datetime.now()

    # https://github.com/facebookresearch/faiss/wiki/Faiss-indexes
    index = faiss.IndexFlatIP(d)  # build the index
    # print(index.is_trained)

    index.add(xb)  # add vectors to the index

    end = datetime.datetime.now()

    index_time = (end - start).microseconds

    print("### Building index costs %s" % (time_str(index_time)))

    print("### Start to secarch all queries")
    start = datetime.datetime.now()
    D, I = index.search(xq, topk)  # actual search

    print(I[:5])  # neighbors of the 5 first queries
    print(I[-5:])  # neighbors of the 5 last queries
    end = datetime.datetime.now()

    search_time = (end - start).microseconds

    print("### Total search time %s" % (time_str(search_time)))
    print("### Avg cost per query: %s" % (time_str(search_time / nq)))

    result_file = "results.csv"

    if os.path.isfile(result_file):
        with open(result_file, "a") as output:
            output.write("%d,%d,%d,%d,%f,%f,%f,%f\n" % (
            nb, nq, d, topk, generate_data_time / 1000, index_time / 1000, search_time / 1000, search_time / nq / 1000))
    else:
        with open(result_file, "w") as output:
            output.write(
                "nb, nq, d, topk, generate_data_time (millisecs), index_time (millisecs), search_time (millisecs), search_time / nq (millisecs)\n")
