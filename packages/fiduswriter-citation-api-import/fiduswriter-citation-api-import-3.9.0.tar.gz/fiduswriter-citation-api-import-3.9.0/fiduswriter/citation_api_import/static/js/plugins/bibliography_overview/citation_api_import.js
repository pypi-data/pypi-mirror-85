import {BibLatexApiImporter} from "../../modules/citation_api_import"

export class BibLatexApiImporterBibliographyOverview {
    constructor(bibliographyOverview) {
        this.bibliographyOverview = bibliographyOverview
    }

    init() {
        this.addButton()
    }

    addButton() {
        this.bibliographyOverview.menu.model.content.push({
            type: 'text',
            icon: 'database',
            title: gettext('Import from Database'),
            action: overview => {
                const apiImporter = new BibLatexApiImporter(
                    overview.app.bibDB,
                    ids => overview.updateTable(ids)
                )
                apiImporter.init()
            }
        })
        this.bibliographyOverview.menu.update()
    }

}
