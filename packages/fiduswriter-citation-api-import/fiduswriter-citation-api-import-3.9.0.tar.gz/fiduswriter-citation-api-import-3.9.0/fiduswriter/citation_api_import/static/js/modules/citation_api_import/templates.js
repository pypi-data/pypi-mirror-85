import {escapeText} from "../common"

export const searchApiTemplate = ({searchers}) =>
    `<p>
        <input id="bibimport-search-text" class="linktitle" type="text" value=""
                placeholder="${gettext("Title, Author, DOI, etc.")}"><br>
        ${searchers.map(searcher => `<input type="checkbox" class="bibimport-search-enabled" id="bibimport-enable-${searcher.id}">&nbsp;${escapeText(searcher.name)}`).join(' ')}
        <button id="bibimport-search-button" class="fw-button fw-dark" type="button">
            ${gettext("search")}
        </button>
    </p>
    <div id="bibimport-search-header"></div>
    ${searchers.map(searcher => `<div id="bibimport-search-result-${searcher.id}" class="bibimport-search-result"></div>`).join('')}`

export const searchApiResultGesisTemplate = ({items}) => {
    return '<h3 class="fw-green-title">GESIS Search</h3><table class="fw-data-table fw-large dataTable-table">' +
        `<tr>
            <th></th>
            <th>${gettext('Title')}</th>
            <th>${gettext('Author(s)')}</th>
            <th>${gettext('Published')}</th>
            <th>${gettext('Abstract')}</th>
        </tr>` +
        items.map(item => {
            const itemTitle = item.title ? typeof item.title === 'object' ? item.title[0] : item.title : false
            const itemAbstract = item.abstract ? typeof item.abstract === 'object' ? item.abstract[0] : item.abstract : false
            return `<tr class="item">
                <td><button type="button"
                        class="api-import fw-button fw-orange fw-small"
                        data-id="${item.id}"
                        data-type="${item.type}"
                >
                    ${gettext('Import')}
                </button></td>
                <td>
                ${
    itemTitle ?
        `<h3>
                        ${escapeText(itemTitle)}
                    </h3>` :
        ''
}
                </td>
                <td>
                ${
    item.person && item.person.length ?
        `<p>
                        ${item.person.join("; ")}
                    </p>` :
        ''
}
                </td>
                <td>
                ${
    item.date ?
        `<p>${item.date}</p>` :
        ''
}
                </td>
                <td>
                ${
    itemAbstract ?
        `<p>
                        ${
    itemAbstract.length < 200 ?
        escapeText(itemAbstract) :
        escapeText(itemAbstract.substring(0, 200)) + "..."
}
                    </p>` :
        ''
}
                </td>
            </tr>`
        }).join('') + '</table>'
}

export const searchApiResultDataciteTemplate = ({items}) => {
    return '<h3 class="fw-green-title">Datacite</h3><table class="fw-data-table fw-large dataTable-table">' +
        `<tr>
            <th></th>
            <th>${gettext('Title')}</th>
            <th>${gettext('Author(s)')}</th>
            <th>${gettext('Published')}</th>
            <th>${gettext('DOI')}</th>
            <th>${gettext('Description')}</th>
        </tr>` +
        items.map(item =>
            `<tr class="item">
                <td><button type="button" class="api-import fw-button fw-orange fw-small"
                        data-doi="${item.doi}">
                    ${gettext('Import')}
                </button></td>
                <td><h3>
                    ${escapeText(item.title)}
                </h3></td>
                <td>
                ${
    item.author ?
        `<p>
                        ${
    item.author.map(author =>
        author.literal ?
            author.literal :
            `${author.family} ${author.given}`
    ).join(", ")
}
                    </p>` :
        ''
}
                </td>
                <td>
                ${
    item.published ?
        `<p>${item.published}</p>` :
        ''
}
                </td>
                <td>
                ${
    item.doi ?
        `<p>${item.doi}</p>` :
        ''
}
                </td>
                <td>
                ${
    item.description ?
        `<p>
                        ${
    item.description.length < 200 ?
        escapeText(item.description) :
        escapeText(item.description.substring(0, 200)) + "..."
}
                    </p>` :
        ''
}
                </td>
            </tr>`
        ).join('') + '</table>'
}


export const searchApiResultPubmedTemplate = ({items}) => {
    return '<h3 class="fw-green-title">Pubmed</h3><table class="fw-data-table fw-large dataTable-table">' +
        `<tr>
            <th></th>
            <th>${gettext('Title')}</th>
            <th>${gettext('Author(s)')}</th>
            <th>${gettext('Published')}</th>
            <th>${gettext('PMID')}</th>
        </tr>` +
        items.map(item =>
            `<tr class="item">
                <td><button type="button" class="api-import fw-button fw-orange fw-small"
                        data-pmid="${item.pmid}">
                    ${gettext('Import')}
                </button></td>
                <td><h3>
                    ${item.title}
                </h3></td>
                <td>
                    <p>${item.authors}</p>
                </td>
                <td>
                    <p>${item.published}</p>
                </td>
                <td>
                    <p>${item.pmid}</p>
                </td>
            </tr>`
        ).join('') + '</table>'
}


export const searchApiResultCrossrefTemplate = ({items}) => {
    return '<h3 class="fw-green-title">Crossref</h3><table class="fw-data-table fw-large dataTable-table">' +
        `<tr>
            <th></th>
            <th>${gettext('Title/Year')}</th>
            <th>${gettext('DOI')}</th>
            <th>${gettext('Description')}</th>
        </tr>` +
        items.map(item =>
            `<tr class="item">
                <td><button type="button" class="api-import fw-button fw-orange fw-small"
                        data-doi="${item.doi.replace(/https?:\/\/(dx\.)?doi\.org\//gi, '')}">
                    ${gettext('Import')}
                </button></td>
                <td><h3>
                    ${
    item.fullCitation ?
        item.fullCitation :
        `${item.title} ${item.year}`
}
                </h3></td>
                <td>
                ${
    item.doi ?
        `<p>${item.doi}</p>` :
        ''
}
                </td>
                <td>
                ${
    item.description ?
        `<p>
                        ${
    item.description.length < 200 ?
        escapeText(item.description) :
        escapeText(item.description.substring(0, 200)) + "..."
}
                    </p>` :
        ''
}
                </td>
            </tr>`
        ).join('') + '</table>'
}
