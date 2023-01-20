from edgar import Company, TXTML


def download_10k_filings(cik):
    company = Company(cik, cik)
    filings = company.get_all_filings(filing_type="10-K")
    url_groups = company._group_document_type(filings, "10-K")
    for url_group in url_groups:
        for url in url_group:
            url = f"https://www.sec.gov{url}"
            print(url)
            txtml = TXTML(url)
            print(txtml.get_text())
            break
        break
    return
