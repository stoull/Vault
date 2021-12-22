/// 将其它所有的全局变量都绑定到这个唯一的全局变量，而非默认的window上
var Vault = {}

function showAlert(message) {
	alert(message);
}

function updateHeading() {
	document.getElementById('heading').innerHTML = "Heading changed with JS";
}

// fetch('http://example.com/movies.json')
//   .then(response => response.json())
//   .then(data => console.log(data));


function httpGetSideTableJsonDataAndUpdateUI()
{
	const movie_json_url = "movie.json"
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            let resultJson = JSON.parse(xmlHttp.response);
            createSideTable(resultJson);
        } else {
            // alert("错误：" + xmlHttp.readyState)
        }
    }
    xmlHttp.open("GET", movie_json_url, true); // true for asynchronous 
    xmlHttp.send(null);
}

// 创建后台编辑页sider bar table
function createSideTable(nameArray) {
    let side_bar = document.getElementById('side_bar');
    let tbl = document.createElement('table');
    tbl.setAttribute('id', 'Database_tables');
    tbl.setAttribute('class', 'side_index');
    let tbdy = document.createElement('tbody');
    for (let i = 0; i < nameArray.length; i++) {
        let tr = document.createElement('tr');
        tr.setAttribute('class', 'side_index')
        tr.appendChild(document.createTextNode(nameArray[i]))
        tr.onclick = function() {
            sideRowDidClick(this);
        }
        // for (let j = 0; j < nameArray.length; j++) {
        //     let td = document.createElement('td');
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
    let text = row.innerText || row.textContent;
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