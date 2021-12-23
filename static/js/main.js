/// 将其它所有的全局变量都绑定到这个唯一的全局变量，而非默认的window上
var Vault = {}

function showAlert(message) {
	alert(message);
}

function updateHeading() {
	document.getElementById('heading').innerHTML = "Heading changed with JS";
}

Vault.jsonHttp = new XMLHttpRequest();

function httpGetSideTableJsonDataAndUpdateUI()
{
	const table_json_url = "/json/tables";
    // let jsonHttp = new XMLHttpRequest();
    Vault.jsonHttp.onload = function() { 
        if (Vault.jsonHttp.readyState == 4 && Vault.jsonHttp.status == 200) {
            let resultJson = JSON.parse(Vault.jsonHttp.response);
            createSideTable(resultJson);
        } else {
            // alert("错误：" + jsonHttp.readyState)
        }
    }
    Vault.jsonHttp.open("GET", table_json_url, true); // true for asynchronous 
    Vault.jsonHttp.send(null);
}

// 获取对应的表数据，并更新显示
function httpGetTableContentDataAndUpdateUI(tableName) {
    let content_url = "/json/content".concat("/", tableName)
    Vault.jsonHttp.open('GET', content_url, true) // true 表示异步
    Vault.jsonHttp.onload = function (e) {
        if (Vault.jsonHttp.readyState == 4 && Vault.jsonHttp.status == 200) {
            let resultJson = JSON.parse(Vault.jsonHttp.response);
            // console.log(resultJson)
            createContentTable(resultJson, tableName)
        } else {
            console.error(Vault.jsonHttp.statusText);
        }
    }
    Vault.jsonHttp.onerror = function (e) {
        console.error(Vault.jsonHttp.statusText);
    }
    Vault.jsonHttp.send(null);
}

// 创建后台编辑页内容视图
function createContentTable(jsonData, tableName) {
    let contentArea = document.getElementById('content_area');
    contentArea.innerHTML = "<h2>详情</h2>"
    let tbl = document.createElement('table');
    tbl.setAttribute('id','content_table');
    tbl.setAttribute('class','data_content');
    let tdby = document.createElement('tbody');
    for (let i=0; i < jsonData.length; i++) {
        let row = jsonData[i];
        let tr = document.createElement('tr');
        tr.setAttribute('class', 'data_content');
        for (let j=0; j<row.length; j++) {
            let td = document.createElement('td');
            td.setAttribute('class', 'data_content');
            console.log(tableName);
            if (tableName == "movie") {
                let divCon = document.createElement('div');
                divCon.setAttribute('style','height:60px; overflow:hidden');
                divCon.appendChild(document.createTextNode(row[j]));
                td.appendChild(divCon);
            } else {
                td.appendChild(document.createTextNode(row[j]));
            }
            
            tr.appendChild(td);
        }
        tdby.appendChild(tr);
    }
    tbl.appendChild(tdby);
    contentArea.appendChild(tbl);
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
        // for (let j = 0; j < 2; j++) {
        //     let td = document.createElement('td');
        //     td.appendChild(document.createTextNode("I'm td"))
        //     td.setAttribute('class', 'side_index')
        //     tr.appendChild(td)
        // }
        tbdy.appendChild(tr);
    }
    tbl.appendChild(tbdy);
    side_bar.appendChild(tbl);
}

function sideRowDidClick(row) {
    let text = row.innerText || row.textContent;
    console.log(text)
    httpGetTableContentDataAndUpdateUI(text)
}




// 显示对应的编辑页
function showEditWithContent(tableName) {
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