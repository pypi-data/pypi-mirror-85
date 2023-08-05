import {get} from "../common"

import {searchApiResultPubmedTemplate} from "./templates"

export class PubmedSearcher {

    constructor(importer) {
        this.importer = importer
        this.id = 'pubmed'
        this.name = 'Pubmed'
    }

    bind() {
        document.querySelectorAll('#bibimport-search-result-pubmed .api-import').forEach(resultEl => {
            const pmid = resultEl.dataset.pmid
            resultEl.addEventListener('click', () => this.getBibtex(pmid))
        })
    }

    lookup(searchTerm) {

        return get(`/proxy/citation_api_import/https://www.bioinformatics.org/texmed/cgi-bin/query.cgi`, {query: escape(searchTerm)}).then(
            response => response.text()
        ).then(
            html => {
                const doc = new DOMParser().parseFromString(html, "text/html")
                const items = Array.from(doc.querySelectorAll('form p')).map(el => {
                    if (el.textContent.length === 0) {
                        return false
                    }
                    const pmid = el.querySelector('input[name="PMID"]').value
                    const descriptionParts = el.innerHTML.split('<br>\n')[1].split(/ <b>\(|\)<\/b>\. /g)
                    return {pmid, authors: descriptionParts[0], published: descriptionParts[1], title: descriptionParts[2]}
                }).filter(item => item)
                const searchEl = document.getElementById('bibimport-search-result-pubmed')
                if (!searchEl) {
                    // window was closed before result was ready.
                    return
                }
                if (items.length) {
                    searchEl.innerHTML = searchApiResultPubmedTemplate({items})
                } else {
                    searchEl.innerHTML = ''
                }
                this.bind()
            }

        )
    }

    getBibtex(pmid) {
        this.importer.dialog.close()
        return get(`/proxy/citation_api_import/https://www.bioinformatics.org/texmed/cgi-bin/list.cgi`, {PMID: pmid}).then(
            response => response.text()
        ).then(
            html => {
                const doc = new DOMParser().parseFromString(html, "text/html")
                const bibtex = doc.querySelector('pre').innerHTML
                return this.importer.importBibtex(bibtex)
            }
        )
    }

}
