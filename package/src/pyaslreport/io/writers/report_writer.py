class ReportWriter:

    @staticmethod
    def write(report, filepath):
        with open(filepath, 'w') as file:
            file.write(report)
