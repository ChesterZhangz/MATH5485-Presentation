from pathlib import Path


class TexPlot:
    """The plot commands used by the exercises, rendered with PGFPlots."""

    colors = ("blue!65!black", "orange!85!black", "green!45!black", "red")
    markers = {"o": "*", "s": "square*", "d": "diamond*"}
    legend_positions = {
        "lower left": "south west",
    }

    def __init__(self):
        self.options = {
            "width": "7in", "height": "4in", "grid": "none",
            "legend cell align": "left", "legend pos": "north east",
            "scaled ticks": "false",
        }
        self.curves = []
        self.color_index = 0
        self.x_limits = []

    def plot(self, x, y, fmt="", *, label, color=None, marker=None,
             linestyle=None, **_):
        if fmt.startswith("k"):
            color = "black"
        if color is None:
            color = self.colors[self.color_index % len(self.colors)]
            self.color_index += 1
        if marker is None:
            marker = next((symbol for symbol in self.markers if symbol in fmt), None)
        style = [color, "thick"]
        if "--" in fmt or linestyle == "--":
            style.append("dashed")
        if marker is not None:
            style.extend([f"mark={self.markers[marker]}", "mark size=1.5pt"])

        self.x_limits.extend([min(x), max(x)])
        points = " ".join(f"({a:.10g},{b:.10g})" for a, b in zip(x, y))
        self.curves.append(
            rf"\addplot[{','.join(style)}] coordinates {{{points}}};"
            + "\n" + rf"\addlegendentry{{{label}}}"
        )

    def loglog(self, x, y, *args, **kwargs):
        self.options.update(xmode="log", ymode="log")
        self.plot(x, y, *args, **kwargs)

    def axhline(self, y, **kwargs):
        self.plot([min(self.x_limits), max(self.x_limits)], [y, y], **kwargs)

    def set_xlabel(self, label):
        self.options["xlabel"] = "{" + label + "}"

    def set_ylabel(self, label):
        self.options["ylabel"] = "{" + label + "}"

    def set_title(self, title):
        self.options["title"] = "{" + title + "}"

    def set_xticks(self, ticks, labels=None, *, minor=False):
        if minor:
            return
        self.options["xtick"] = "{" + ",".join(map(str, ticks)) + "}"
        if labels is not None:
            self.options["xticklabels"] = "{" + ",".join(
                "{" + label + "}" for label in labels
            ) + "}"

    def set_yticks(self, ticks):
        self.options["ytick"] = "{" + ",".join(map(str, ticks)) + "}"

    def legend(self, *, loc="upper right"):
        self.options["legend pos"] = self.legend_positions.get(loc, "north east")
        if loc == "center right":
            self.options["legend style"] = "{at={(0.98,0.53)},anchor=east}"

    def savefig(self, filename):
        tex = Path(filename).with_suffix(".tex")
        options = ",\n".join(f"{key}={value}" for key, value in self.options.items())
        tex.write_text(
            r"\begin{tikzpicture}" "\n"
            rf"\begin{{axis}}[{options}]" "\n"
            + "\n".join(self.curves) + "\n"
            r"\end{axis}\end{tikzpicture}" "\n",
            encoding="utf-8",
        )
