import json
import os

import numpy
import pylab


base_path = os.path.join(
    "log", "Linux-CPython-{}-64bit".format(os.environ["PYTHONVERSION"])
)
for counter in ["0001", "0002"]:
    results = dict()
    try:
        with open(
            os.path.join(
                base_path,
                "{}_benchmark_py{}_{}.json".format(
                    counter,
                    os.environ["PYTHONVERSION"].replace(".", ""),
                    os.environ["PYTHONUPDATE"],
                ),
            )
        ) as json_file:
            for stats in json.load(json_file)["benchmarks"]:
                try:
                    params = stats["param"].split("-")
                    group, pkg, fun = (
                        stats["fullname"]
                        .replace(".py::test", "")
                        .split("[", 1)[0]
                        .split("_")[1:]
                    )
                    if len(params) == 2:
                        ptype, porder = params
                    elif len(params) == 3:
                        fun, ptype, porder = params
                except BaseException:
                    continue
                if pkg not in results:
                    results[pkg] = dict()
                if group not in results[pkg]:
                    results[pkg][group] = dict()
                if fun not in results[pkg][group]:
                    results[pkg][group][fun] = dict()
                if ptype not in results[pkg][group][fun]:
                    results[pkg][group][fun][ptype] = dict()
                if porder not in results[pkg][group][fun][ptype]:
                    results[pkg][group][fun][ptype][porder] = stats["stats"][
                        "ops"
                    ]
    except BaseException:
        continue

    figs_axes = dict()
    if "numpy" in results:
        for group in results["numpy"].keys():
            for fun in results["numpy"][group].keys():
                for ptype in results["ipps"][group][fun].keys():
                    fig_name = "{}_{}".format(group, ptype)
                    if fig_name not in figs_axes:
                        fig = pylab.figure(figsize=(8.25, 8.25))
                        ax = fig.add_subplot(111)
                        figs_axes[fig_name] = (fig, ax)

                    data_ipps = numpy.asarray(
                        [
                            [int(k), results["ipps"][group][fun][ptype][k]]
                            for k in results["ipps"][group][fun][ptype].keys()
                        ]
                    )
                    ind = numpy.argsort(data_ipps[:, 0])
                    data_ipps = data_ipps[ind, :]
                    data_numpy = numpy.asarray(
                        [
                            [int(k), results["numpy"][group][fun][ptype][k]]
                            for k in results["ipps"][group][fun][ptype].keys()
                        ]
                    )
                    ind = numpy.argsort(data_numpy[:, 0])
                    data_numpy = data_numpy[ind, :]

                    L1_eff, L2_eff = 100 * data_ipps[:, 1] / data_numpy[:, 1]
                    if L2_eff > 105 and L1_eff > 105:
                        figs_axes[fig_name][1].scatter(
                            L1_eff,
                            L2_eff,
                            c="C0",
                        )
                    elif L1_eff > 95 and L2_eff > 95:
                        figs_axes[fig_name][1].scatter(
                            L1_eff,
                            L2_eff,
                            c="C1",
                        )
                    else:
                        figs_axes[fig_name][1].scatter(
                            L1_eff,
                            L2_eff,
                            c="C3",
                        )
                    figs_axes[fig_name][1].annotate(fun, (L1_eff, L2_eff))

    for fig_name, (fig, ax) in figs_axes.items():
        ax.set_xscale("log")
        ax.set_yscale("log")

        L1_lim = ax.get_xlim()
        L2_lim = ax.get_ylim()

        ax.plot([100, L1_lim[1]], [95, 95], "k:")
        ax.plot([100, L1_lim[1]], [100, 100], "k--")
        ax.plot([100, L1_lim[1]], [105, 105], "k:")
        ax.plot([95, 95], [100, L2_lim[1]], "k:")
        ax.plot([100, 100], [100, L2_lim[1]], "k--")
        ax.plot([105, 105], [100, L2_lim[1]], "k:")

        ax.set_xlabel("IPP vs Numpy Ratio -- L1 Cache (%)")
        ax.set_ylabel("IPP vs Numpy Ratio -- L2 Cache (%)")

        fig.tight_layout()
        fig.savefig(
            os.path.join(base_path, "{}-{}.svg".format(counter, fig_name))
        )
