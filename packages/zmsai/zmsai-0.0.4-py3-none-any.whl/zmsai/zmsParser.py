#!/usr/bin/env python3
import argparse
import zmsai.base as base
from zmsai.LDA import heuristics
from zmsai.readData import read_txt
import pickle as pkl

import os

import warnings

warnings.filterwarnings("ignore")


def main():
    args = argparse.ArgumentParser()
    args.add_argument("task", nargs="?", default="run", help=base.helpTask)
    args.add_argument("--path", "-p", nargs="?", default=base.path, help=base.helpPath)
    args.add_argument(
        "--topics", "-t", nargs="?", default=base.numberTopics, help=base.helpTopics
    )
    args.add_argument(
        "--nwords", "-w", nargs="?", default=base.nWords, help=base.helpnWords
    )
    args.add_argument(
        "--distro", "-d", nargs="?", default=base.defaultDistro, help=base.helpDistro
    )

    pargs = args.parse_args()
    ndoc, docs = countFiles(pargs.path)
    if pargs.task == "run":
        print(base.run)
        if os.path.exists("meta.zms"):
            os.remove("meta.zms")
        distributions = heuristics(path=pargs.path, numberTopics=int(pargs.topics))
        distributions.save()
        pass
    elif pargs.task == "test":
        print(base.run)
        if os.path.exists("meta.zms"):
            os.remove("meta.zms")
        distributions = heuristics(path=pargs.path, numberTopics=int(pargs.topics))
        distributions.get_doc_topic_distrib(docs)
        distributions.get_topic_word_distrib(int(pargs.nwords))
        distributions.get_doc_word_distrib(docs, int(pargs.nwords))
        distributions.get_vocabulary(docs, int(pargs.nwords))
        pass

    elif pargs.task == "display":
        if os.path.exists("meta.zms"):
            pass
        else:
            choice = input(base.choice)
            if choice == "y":
                print(base.run)
                distributions = heuristics(
                    path=pargs.path, numberTopics=int(pargs.topics)
                )
                distributions.save()
            else:
                print("Taking it as a no.")
                return
        pickling_on = open("meta.zms", "rb")
        distributions = pkl.load(pickling_on)

        if pargs.distro == "dt":
            distributions.get_doc_topic_distrib(docs)
        elif pargs.distro == "tw":
            distributions.get_topic_word_distrib(int(pargs.nwords))
        elif pargs.distro == "dw":
            distributions.get_doc_word_distrib(docs, int(pargs.nwords))
        elif pargs.distro == "voc":
            distributions.get_vocabulary(docs, int(pargs.nwords))
        elif pargs.distro == "all":
            distributions.get_doc_topic_distrib(docs)
            distributions.get_topic_word_distrib(int(pargs.nwords))
            distributions.get_doc_word_distrib(docs, int(pargs.nwords))
            distributions.get_vocabulary(docs, int(pargs.nwords))

        pass

    elif pargs.task == "delete":
        pickling_on = open("meta.zms", "rb")
        from sys import getsizeof as size

        obj = pkl.load(pickling_on)
        os.remove("meta.zms")
        print(base.delete, size(obj) / 1024, "kb freed")
        pass

    elif pargs.task == "man":
        USAGE = open("MAN.txt", "r")
        print(USAGE.read())
        pass

    else:
        print("[Invalid argument]")
        pass


def countFiles(DIR):
    from os import listdir

    lsdir = listdir(DIR)
    count = len(lsdir)
    return count, lsdir


if __name__ == "__main__":
    main()
