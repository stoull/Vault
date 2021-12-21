function showAlert(message) {
	alert(message);
}

function updateHeading() {
	document.getElementById('heading').innerHTML = "Heading changed with JS";
}

// fetch('http://example.com/movies.json')
//   .then(response => response.json())
//   .then(data => console.log(data));


function httpGetMovieJsonData()
{
	let movie_json_url = "movie.json"
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            var result = JSON.parse(xmlHttp.response);
        	console.log(result);
            createSideTable(result);
        // else
            // alert("错误：" + xmlHttp.readyState)
    }
    xmlHttp.open("GET", movie_json_url, true); // true for asynchronous 
    xmlHttp.send(null);
}

// 创建后台编辑页sider bar table
function createSideTable(nameArray) {
    var side_bar = document.getElementById('side_bar');
    var tbl = document.createElement('table');
    tbl.setAttribute('id', 'Database_tables');
    tbl.setAttribute('class', 'side_index');
    var tbdy = document.createElement('tbody');
    for (var i = 0; i < nameArray.length; i++) {
        var tr = document.createElement('tr');
        tr.setAttribute('class', 'side_index')
        tr.appendChild(document.createTextNode(nameArray[i]))
        tr.onclick = function() {
            sideRowDidClick(this);
        }
        // for (var j = 0; j < nameArray.length; j++) {
        //     var td = document.createElement('td');
        //     td.appendChild(document.createTextNode(nameArray[j]))
        //     td.setAttribute('class', 'side_index')
        //     tr.appendChild(td)
        // }
        tbdy.appendChild(tr);
    }
    tbl.appendChild(tbdy);
    side_bar.appendChild(tbl)
}

function sideRowDidClick(row) {
    var text = row.innerText || row.textContent;
    console.log(text)
}




// function httpGetAsync(theUrl, callback)
// {
//     var xmlHttp = new XMLHttpRequest();
//     xmlHttp.onreadystatechange = function() { 
//         if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
//             callback(xmlHttp.responseText);
//     }
//     xmlHttp.open("GET", theUrl, true); // true for asynchronous 
//     xmlHttp.send(null);
// }

// fetch(url).then(function(response) {
//   return response.json();
// }).then(function(data) {
//   console.log(data);
// }).catch(function() {
//   console.log("Booo");
// });



// function drawRow(nameArray) {
//     for(var i = 0; i < nameArray.length; i++) {
//         var row = $("<tr />")
//         $("#Database_tables").append(row); 
//         var obj = nameArray[i];
//         row.append($("<td>" + obj + "</td>"));
//     }
// }