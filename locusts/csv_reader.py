import csv


class CSVReader:
    """
    Leitor de CSV
    """

    def __init__(self, file_path: str) -> None:
        """
        Construtor.
        """

        self.file_path = file_path

    def read(self) -> list[dict]:
        """
        Le o arquivo csv.
        """

        reader = csv.DictReader(open(self.file_path))
        data: list[dict] = []
        for element in reader:
            data.append(element)

        return data
