import {searchApiResultCrossrefTemplate} from "./templates"

export class CrossrefSearcher {

    constructor(importer) {
        this.importer = importer
        this.id = 'crossref'
        this.name = 'Crossref'
    }

    bind() {
        document.querySelectorAll('#bibimport-search-result-crossref .api-import').forEach(resultEl => {
            const doi = resultEl.dataset.doi
            resultEl.addEventListener('click', () => this.getBibtex(doi))
        })
    }

    lookup(searchTerm) {
        return fetch(`https://search.crossref.org/dois?q=${encodeURIComponent(escape(searchTerm))}`, {
            method: "GET",
        }).then(
            response => response.json()
        ).then(items => {
            const searchEl = document.getElementById('bibimport-search-result-crossref')
            if (!searchEl) {
                // window was closed before result was ready.
                return
            }
            if (items.length) {
                searchEl.innerHTML = searchApiResultCrossrefTemplate({items})
            } else {
                searchEl.innerHTML = ''
            }
            this.bind()
        })
    }

    getBibtex(doi) {
        this.importer.dialog.close()
        fetch(`https://search.crossref.org/citation?format=bibtex&doi=${doi}`, {
            method: "GET"
        }).then(
            response => response.text()
        ).then(
            bibtex => this.importer.importBibtex(bibtex)
        )
    }

}
