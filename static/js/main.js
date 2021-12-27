/// 将其它所有的全局变量都绑定到这个唯一的全局变量，而非默认的window上
var Vault = {}

Vault.jsonHttp = new XMLHttpRequest();


class Movie {
    constructor(json) {
        id = json['id']
        
    }
}


// 获取最新添加的电影数据
function httpGetTheLastUpdateAndUpdateUI() {
    let lastUpdateUrl = "/json/content/movie";
    Vault.jsonHttp.open('GET', lastUpdateUrl);
    Vault.jsonHttp.onload = function (e) {
        if (Vault.jsonHttp.readyState == 4 && Vault.jsonHttp.status == 200) {
            let jsonResult = JSON.parse(Vault.jsonHttp.response);
            createTheLastNews(jsonResult);
            // console.log("httpGetTheLastUpdateAndUpdateUI " + jsonResult)
        } else {
            console.error(Vault.jsonHttp.statusText);
        }
    }
    Vault.jsonHttp.onerror = function (e) {
        console.error(Vault.jsonHttp.statusText);
    }
    Vault.jsonHttp.send(null);
}

// 获取数据库tables
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
            updateSideTable(tableName)
        } else {
            console.error(Vault.jsonHttp.statusText);
        }
    }
    Vault.jsonHttp.onerror = function (e) {
        console.error(Vault.jsonHttp.statusText);
    }
    Vault.jsonHttp.send(null);
}


// ==========  首页 ==========
function createTheLastNews(movieList) {
    let contentTbl = document.getElementById('last_update_table');
    for (let i=0; i < movieList.length; i++) {
        let tr = document.createElement('tr');
        for (let j=0; j<4; j++) {
            let td = document.createElement('td');
            td.setAttribute('class', 'data_content');
            let valueIndex = j;
            if (j == 0) {
                valueIndex = 1
            } else if (j == 1) {
                valueIndex = 7
                td.setAttribute('style', 'text-align: left;')
            } else if (j == 2) {
                valueIndex = 6
            } else {
                valueIndex = 12
            }
            td.appendChild(document.createTextNode(movieList[i][valueIndex]))
            tr.appendChild(td)
            tr.onclick = function() {
                showMoviePage(this)
            }
        }
        contentTbl.appendChild(tr)
    }
}

function showMoviePage(movieTr) {
    let movieName = movieTr.children[0].innerText
    console.log("Show the detail of movie name: " + movieName)
}



// ==========  后台编辑页 ==========

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
            let divCon = document.createElement('div');
            divCon.setAttribute('style','display: table-cell; vertical-align: middle;');
            divCon.appendChild(document.createTextNode(row[j]));
            td.appendChild(divCon);
            // td.appendChild(document.createTextNode(row[j]));
            
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
    tbdy.setAttribute('id', 'Database_tables_body');
    for (let i = 0; i < nameArray.length; i++) {
        let tr = document.createElement('tr');
        tr.setAttribute('class', 'side_tr_wapper')
        tr.appendChild(document.createTextNode(nameArray[i]))
        tr.onclick = function() {
            sideRowDidClick(this);
        }
        let eidtButton = document.createElement('Button')
        let image = document.createElement('img')
        image.src = "/static/images/edit_small_blue.png"
        eidtButton.setAttribute('class','edit')
        eidtButton.appendChild(image)
        eidtButton.onclick = function() {
            sideRowDidClickEdit(this)
        }
        tr.appendChild(eidtButton)
        tbdy.appendChild(tr);
    }
    tbl.appendChild(tbdy);
    side_bar.appendChild(tbl);
}

function updateSideTable(tableName) {
    let tableNames = new Array()
    let tbdy = document.getElementById('Database_tables_body');
    for (let i=0; i<tbdy.children.length; i++) {
        let trObj = tbdy.children[i];
        let innerText = trObj.innerText;
        trObj.setAttribute('class', 'side_tr_wapper');
        if (innerText == tableName) {
            trObj.setAttribute('class', 'side_tr_wapper_selected');
        }
        // tableNames.push(innerText);
    }
}


function sideRowDidClick(row) {
    let text = row.innerText || row.textContent;
    // console.log(text)
    httpGetTableContentDataAndUpdateUI(text)
}

// 显示对应的编辑页
function sideRowDidClickEdit(row) {
    let text = ""
    try {
        text = row.closest('.side_tr_wapper').innerText
    } catch (error){
        text = row.closest('.side_tr_wapper_selected').innerText
    }
    // console.log(text)
    alert("改功能暂未开放！您尝试编辑： " + text);
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