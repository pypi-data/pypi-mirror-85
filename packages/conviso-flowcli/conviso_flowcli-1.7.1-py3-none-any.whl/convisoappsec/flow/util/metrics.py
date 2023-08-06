from convisoappsec.flow.source_code_scanner import SCC


def project_metrics(source_code_dir):
    scanner = SCC(source_code_dir)
    scanner.scan()

    return {
        'total_lines': scanner.total_source_code_lines
    }
