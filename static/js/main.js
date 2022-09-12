/// 将其它所有的全局变量都绑定到这个唯一的全局变量，而非默认的window上
var Vault = {}

Vault.jsonHttp = new XMLHttpRequest();


// class Movie {
//     constructor(json) {
//         id = json['id']
        
//     }
// }


// 获取最新添加的电影数据
function httpGetTheLastUpdateAndUpdateUI() {
    let lastUpdateUrl = "/json/movie/theLastMovies";
    Vault.jsonHttp.open('POST', lastUpdateUrl);
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
    Vault.jsonHttp.open("POST", table_json_url, true); // true for asynchronous 
    Vault.jsonHttp.send(null);
}

// 获取对应的表数据，并更新显示
function httpGetTableContentDataAndUpdateUI(tableName) {
    let content_url = "/json/content".concat("/", tableName)
    Vault.jsonHttp.open('POST', content_url, true) // true 表示异步
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
    console.log(movieList)
    let contentDiv = document.getElementById('last_update_gallery');
    for (let i=0; i < movieList.length; i++) {
        let movie = movieList[i]
        let a_item = document.createElement('a');
        a_item.setAttribute('href','login');
        a_item.setAttribute('target','_blank');
        a_item.setAttribute('class','default');

        let img_item = document.createElement('img');
        img_item.setAttribute('alt', movie['name']);
        img_item.setAttribute('src',"/static/images/poster/" + movie['poster_name']);
        img_item.setAttribute('class','gallery_item');

        let info_div = document.createElement('div');
        info_div.setAttribute('class','gallery_info_item');

        let title_item = document.createElement('p');
        title_item.setAttribute('class','title_s gallery_item');
        title_item.textContent = movie["name"]

        let des_item = document.createElement('p');
        des_item.setAttribute('class','');
        des_item.textContent = movie["year"] + " " + movie["style"]

        let starts_div = document.createElement('div');
        starts_div.setAttribute('class', 'drc-rating drc-subject-info-rating m');

        let score = movie["score"];
        let score_int = Math.round(score);

        let starts_item = document.createElement('span');
        starts_item.setAttribute('class', 'drc-rating-stars drc-subject-info-rating-stars m');
//        starts_item.setAttribute('data-rating', score*0.5);

        let temp_score = score_int;
        for (let i = 0; i < 5; i++) {
            if (temp_score >= 2) {
                let start_item = document.createElement('span');
                start_item.setAttribute('class', 'drc-rating-stars-item drc-rating-stars-item-full m');
                starts_item.appendChild(start_item)
            } else if (temp_score >= 1) {
                let start_item = document.createElement('span');
                start_item.setAttribute('class', 'drc-rating-stars-item drc-rating-stars-item-half m');
                starts_item.appendChild(start_item)
            } else {
                let start_item = document.createElement('span');
                start_item.setAttribute('class', 'drc-rating-stars-item drc-rating-stars-item-gray m');
                starts_item.appendChild(start_item)
            }
            temp_score -= 2;
        }

        let start_item_text = document.createElement('span');
        start_item_text.setAttribute('class', 'drc-rating-num');
        start_item_text.textContent = score.toString();

        starts_item.appendChild(start_item_text)

        starts_div.appendChild(starts_item)

        info_div.appendChild(title_item)
        info_div.appendChild(des_item)
        info_div.appendChild(starts_div)

        a_item.appendChild(img_item)
        a_item.appendChild(info_div)

        contentDiv.appendChild(a_item)
    }
}

function showMoviePage(movieTr) {
    let movieName = movieTr.children[0].innerText
    console.log("Show the detail of movie name: " + movieName)
    window.location = "movie/" + movieName;
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