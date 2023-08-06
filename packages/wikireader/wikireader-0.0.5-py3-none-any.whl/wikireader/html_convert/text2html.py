"""
Converts text to html

Heads are surrounded by equal signs


"""

class ArticleContent:

    def __init__(self, text):
        self._links = []
        self.body = self._make_body(text)

    @property
    def links(self):
        result = []
        for index, link in enumerate(self._links):
            result.append(f"<a href=\"#h{index}\">{link}</a>")
        return '\n'.join(result)

    def _set_head(self, line):
        """
        Counts the lines, removes any equal signs leading and following
        And converts to html value
        """
        split = line.split(" ")
        level = len(split[0])  # count leading '='
        title = " ".join(split[1:-1])
        self._links.append(title)
        index = len(self._links) - 1
        return f"<h{level} id=\"h{index}\">{title}</h{level}>"

    @staticmethod
    def _set_paragraph(line):
        """
        Changes text into p object
        """
        return f"<p>{line}</p>"

    def _change_line(self, line):
        """
        """
        if line.startswith("="):
            return self._set_head(line)
        else:
            return self._set_paragraph(line)

    def _make_body(self, tekst):
        """
        Returns: html
        """
        lines = [
            self._change_line(line.strip())
            for line in
            tekst.split("\n") if line.strip() ]
        return "\n".join(lines)


