from _metrics import scorers


def main():
    """
    snn = sc.from_spec("python", "diff")
    subs = list(utils.from_sl3("data/subs.sl3", nrows=1000))
    snn.fit(subs)
    """

    src, dst = "a=3", "b=4"
    scorer = scorers.from_spec("python", "ast")
    print(scorer.score(src, dst))


if __name__ == '__main__':
    main()
