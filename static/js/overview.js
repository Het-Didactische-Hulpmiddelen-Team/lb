/*
function get() {
    $.get("https://jsonplaceholder.typicode.com/users", function (data) {

        var contentContainer = $("#table");
        contentContainer.empty();

        var table = document.createElement("table")
        table.setAttribute("class", "table")
        table.setAttribute("id", "table")

        var tableHead = document.createElement("thead")
        tableHead.setAttribute("class", "thead-dark")

        var tableHeadRow = document.createElement("tr")

        var tableHeadCell = document.createElement("th")
        tableHeadCell.setAttribute("scope", "col")
        var tableHeadCellText = document.createTextNode("Name")
        tableHeadCell.appendChild(tableHeadCellText)

        var tableHeadCell2 = document.createElement("th")
        tableHeadCell2.setAttribute("scope", "col")
        tableHeadCell2.setAttribute("class", "w-75")
        var tableHeadCell2Text = document.createTextNode("Progress")
        tableHeadCell2.appendChild(tableHeadCell2Text)

        tableHeadRow.appendChild(tableHeadCell)
        tableHeadRow.appendChild(tableHeadCell2)

        tableHead.appendChild(tableHeadRow)

        table.appendChild(tableHead)

        var tableBody = document.createElement("tbody")

        $.each(data, function (i, message) {
            var dummyPercentage = Math.floor(Math.random() * 101);

            var tableRow = document.createElement("tr")

            var tableCellName = document.createElement("td")
            var nameLink = document.createElement("a")
            var nameLinkText = document.createTextNode(message.name)

            nameLink.setAttribute("href", "")
            nameLink.setAttribute("class", "text-body")
            tableCellName.setAttribute("scope", "row")
            tableCellName.setAttribute("class", "text-wrap")

            nameLink.appendChild(nameLinkText)
            tableCellName.appendChild(nameLink)
            tableRow.appendChild(tableCellName)

            var tableCellProgress = document.createElement("td")
            var progressDiv = document.createElement("div")
            var progressDivInner = document.createElement("div")
            var progressDivInnerText = document.createTextNode(dummyPercentage + "%")

            progressDiv.setAttribute("class", "progress")

            var barColor = "progress-bar"
            if (dummyPercentage < 25) {
                barColor = barColor.concat(" bg-danger")
            } else if (dummyPercentage < 50) {
                barColor = barColor.concat(" bg-warning")
            } else if (dummyPercentage < 75) {
                barColor = barColor.concat(" bg-success")
            }
            progressDivInner.setAttribute("class", barColor)

            progressDivInner.setAttribute("role", "progressbar")
            progressDivInner.setAttribute("style", "width: " + dummyPercentage + "%")
            progressDivInner.setAttribute("aria-valuenow", dummyPercentage)
            progressDivInner.setAttribute("aria-valuemin", "0")
            progressDivInner.setAttribute("aria-valuemax", "100")

            progressDivInner.appendChild(progressDivInnerText)
            progressDiv.appendChild(progressDivInner)
            tableCellProgress.appendChild(progressDiv)
            tableRow.appendChild(tableCellProgress)

            tableBody.appendChild(tableRow)
        });

        table.appendChild(tableBody)
        contentContainer.append(table)
    })
}*/

function filter() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchedName");
    filter = input.value.toUpperCase();
    table = document.getElementById("table");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}