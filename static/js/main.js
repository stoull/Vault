/// 将其它所有的全局变量都绑定到这个唯一的全局变量，而非默认的window上
var Vault = {}

Vault.jsonHttp = new XMLHttpRequest();

// class Movie {
//     constructor(json) {
//         id = json['id']
        
//     }
// }



// 获取最新添加的电影数据
function httpGetTheLastUpdateAndUpdateUI(isGrid) {
    let lastUpdateUrl = "/json/movie/theLastMovies";
    Vault.jsonHttp.open('POST', lastUpdateUrl);
    Vault.jsonHttp.onload = function (e) {
        if (Vault.jsonHttp.readyState == 4 && Vault.jsonHttp.status == 200) {
            let jsonResult = JSON.parse(Vault.jsonHttp.response);
            if (isGrid==true) {
                createTheLastNewsInGrid(jsonResult);
            } else {
                createTheLastNewsTableList(jsonResult);
            }
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

// 视频详情页 获取对应subject 电影id的数据详情
function httpGetSubjectDetail(subjectId) {
    let content_url = "/json/subject".concat("/", subjectId)
    Vault.jsonHttp.open('POST', content_url, true) // true 表示异步
    Vault.jsonHttp.onload = function (e) {
        if (Vault.jsonHttp.readyState == 4 && Vault.jsonHttp.status == 200) {
            let resultJson = JSON.parse(Vault.jsonHttp.response);
            // console.log(resultJson)
            updateSubjectDetailPage(resultJson)
        } else {
            console.error(Vault.jsonHttp.statusText);
        }
    }
    Vault.jsonHttp.onerror = function (e) {
        console.error(Vault.jsonHttp.statusText);
    }
    Vault.jsonHttp.send(null);
}

// 人物详情页 获取对应subject 电影id的数据详情
function httpGetCelebrityDetail(celebrity_id) {
    let content_url = "/json/celebrity".concat("/", celebrity_id)
    Vault.jsonHttp.open('POST', content_url, true) // true 表示异步
    Vault.jsonHttp.onload = function (e) {
        if (Vault.jsonHttp.readyState == 4 && Vault.jsonHttp.status == 200) {
            let resultJson = JSON.parse(Vault.jsonHttp.response);
            // console.log(resultJson)
            updateCelebrityDetailPage(resultJson)
        } else {
            console.error(Vault.jsonHttp.statusText);
        }
    }
    Vault.jsonHttp.onerror = function (e) {
        console.error(Vault.jsonHttp.statusText);
    }
    Vault.jsonHttp.send(null);
}

// 视频详情页 获取对应subject 电影id的评论数据
function httpGetSubjectComments(subjectId) {
    let content_url = "/json/subject".concat("/", subjectId)
    Vault.jsonHttp.open('POST', content_url, true) // true 表示异步
    Vault.jsonHttp.onload = function (e) {
        if (Vault.jsonHttp.readyState == 4 && Vault.jsonHttp.status == 200) {
            let resultJson = JSON.parse(Vault.jsonHttp.response);
            // console.log(resultJson)
            updateSubjectDetailPage(resultJson)
        } else {
            console.error(Vault.jsonHttp.statusText);
        }
    }
    Vault.jsonHttp.onerror = function (e) {
        console.error(Vault.jsonHttp.statusText);
    }
    Vault.jsonHttp.send(null);
}

// 视频播放页 获取对应subject 电影id的数据详情
function httpGetSubjectDetailForPlayer(subjectId) {
    let content_url = "/json/subject".concat("/", subjectId)
    Vault.jsonHttp.open('POST', content_url, true) // true 表示异步
    Vault.jsonHttp.onload = function (e) {
        if (Vault.jsonHttp.readyState == 4 && Vault.jsonHttp.status == 200) {
            let resultJson = JSON.parse(Vault.jsonHttp.response);
            // console.log(resultJson)
            updateVideoPlayerTitle(resultJson)
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
function createTheLastNewsInGrid(movieList) {
    let contentDiv = document.getElementById('content_section');
    contentDiv.innerHTML = '';

    let gallery_div = document.createElement('div');
    gallery_div.setAttribute('class', 'gallery');

    for (let i=0; i < movieList.length; i++) {
        let movie = movieList[i]
        let a_item = document.createElement('a');
        a_item.setAttribute('href','/subject/' + movie['id']);
        a_item.setAttribute('target','_self');
        a_item.setAttribute('class','grid_item');

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

        gallery_div.appendChild(a_item)
    }
    contentDiv.appendChild(gallery_div)
}

// ==========  首页列表图 ==========
function createTheLastNewsTableList(movieList) {
    let contentDiv = document.getElementById('content_section');
    contentDiv.innerHTML = '';

    let content_table = document.createElement('table');
    content_table.setAttribute('class', 'data_content');
    contentDiv.appendChild(content_table)

    // create index header
    let index_tr = document.createElement('tr');
    index_tr.setAttribute('class', 'data_content_tr');

    let indexTitles = ["", "电影名", "年份", "类型", "评分", "介绍", "更新日期"];
    let indexKeys = ["poster_name", "name", "year", "style", "score", "synopsis", "create_date"];
    for (i=0; i<indexTitles.length; i++) {
        let title = indexTitles[i];
        let index_th = document.createElement('th');
        index_th.setAttribute('class', 'data_content_th');
        index_th.textContent = title;
        index_tr.appendChild(index_th);
    }
    content_table.appendChild(index_tr);

    for (let i=0; i < movieList.length; i++) {
        let tr = document.createElement('tr');
        let movie = movieList[i]
        for (let j=0; j<indexTitles.length; j++) {
            let td = document.createElement('td');
            td.setAttribute('class', 'data_content');

            let key = indexKeys[j];
            if (key=="poster_name") {
                let img_item = document.createElement('img');
                img_item.setAttribute('alt', movie['name']);
                img_item.setAttribute('src',"/static/images/poster/" + movie['poster_name']);
                img_item.setAttribute('class','data_content_img');
                td.appendChild(img_item)
            } else {
                td.appendChild(document.createTextNode(movie[key]));
            }

            tr.appendChild(td);
        }
        tr.setAttribute('id', movie['id'])
        tr.onclick = function() {
            showMoviePage(this);
        }
        contentDiv.appendChild(tr);
    }
}

// ==========  电影详情页 ==========
function updateSubjectDetailPage(movie) {
    let movie_id = movie['id'];
    // title
    let titleDiv = document.getElementById('title');

    let hTitle = document.createElement('h');
    hTitle.textContent = movie['name'] + '(' + movie['year'] + ")"

    titleDiv.appendChild(hTitle);

    // poster image
    let coverDiv = document.getElementById('cover');
    coverDiv.innerHTML = '';

    let img_item = document.createElement('img');
    img_item.setAttribute('alt', movie['name']);
    img_item.setAttribute('src',"/static/images/poster/" + movie['poster_name']);
    img_item.setAttribute('class','gallery_item');

    let palyButton = document.createElement('button');
    palyButton.setAttribute('class', 'movie_info_play');
    palyButton.append("Play");
    palyButton.onclick = function() {
        if (movie['is_downloaded'] == "1") {
            window.open("/videoPlayer/"+movie_id, "_self");
        } else {
            alert("文件未下载！")
        }
    }

    coverDiv.appendChild(img_item);
    coverDiv.appendChild(palyButton);

    let detailDiv = document.getElementById('infos');

    detailDiv.appendChild(createDetailLableBlock("导演", movie['directors']));
    detailDiv.appendChild(createDetailLableBlock("编剧", movie['scenarists']));
    detailDiv.appendChild(createDetailLableBlock("演员", movie['actors']));
    detailDiv.appendChild(createDetailLableBlock("类型", movie['style']));
    detailDiv.appendChild(createDetailLableBlock("地区", movie['area']));
    detailDiv.appendChild(createDetailLableBlock("时长", movie['length']));
    detailDiv.appendChild(createDetailLableBlock("其它名称", movie['other_names']));
    detailDiv.appendChild(createDetailLableBlock("评分", movie['score']));
    detailDiv.appendChild(createDetailLableBlock("评分人数", movie['rating_number']));
    detailDiv.appendChild(createDetailLableBlock("位置", movie['filePath']));
    detailDiv.appendChild(createDetailLableBlock("已下载", movie['is_downloaded']));
    detailDiv.appendChild(createDetailLableBlock("", movie['']));
    detailDiv.appendChild(createDetailLableBlock("", movie['']));
    detailDiv.appendChild(createDetailLableBlock("", movie['']));

    detailDiv.appendChild(createDetailLableBlock("简介", movie['synopsis']));

    let introDiv = document.getElementById('intro');
    let introP = document.createElement('p');
    introP.textContent = movie["synopsis"];
    introDiv.appendChild(introP);


//    let introDiv = document.getElementById('comment');


}

// ==========  人物详情页 ==========
function updateCelebrityDetailPage(celebrity) {
    let celebrity_id = celebrity['id'];
    // title
    let titleDiv = document.getElementById('title');

    let hTitle = document.createElement('h');
    hTitle.textContent = celebrity['name']

    titleDiv.appendChild(hTitle);

    // poster image
    let coverDiv = document.getElementById('cover');
    coverDiv.innerHTML = '';

    let img_item = document.createElement('img');
    img_item.setAttribute('alt', celebrity['name']);
    img_item.setAttribute('src',"/static/images/poster/" + celebrity['portrait_name']);
    img_item.setAttribute('class','gallery_item');

    coverDiv.appendChild(img_item);

    let detailDiv = document.getElementById('infos');

    detailDiv.appendChild(createDetailLableBlock("性别", celebrity['gender']));
    detailDiv.appendChild(createDetailLableBlock("星座", celebrity['zodiac']));
    detailDiv.appendChild(createDetailLableBlock("出生日期", celebrity['living_time']));
    detailDiv.appendChild(createDetailLableBlock("出生地", celebrity['birthpalce']));
    detailDiv.appendChild(createDetailLableBlock("职业", celebrity['occupation']));
    detailDiv.appendChild(createDetailLableBlock("中文名", celebrity['names_cn']));
    detailDiv.appendChild(createDetailLableBlock("英文名", celebrity['names_en']));
    detailDiv.appendChild(createDetailLableBlock("家庭成员", celebrity['family']));
    detailDiv.appendChild(createDetailLableBlock("imdb", celebrity['imdb']));

    detailDiv.appendChild(createDetailLableBlock("", celebrity['']));
    detailDiv.appendChild(createDetailLableBlock("", celebrity['']));
    detailDiv.appendChild(createDetailLableBlock("", celebrity['']));

    detailDiv.appendChild(createDetailLableBlock("简介", celebrity['intro']));


//    let introDiv = document.getElementById('intro');
//    let introP = document.createElement('p');
//    introP.textContent = movie["synopsis"];
//    introDiv.appendChild(introP);
}

function createDetailLableBlock(name, values)
{
    let detailP = document.createElement('p');
    detailP.setAttribute('class', 'movie_info_label');
    // detailP.setAttribute('style', 'display: inline;');

    if (typeof values == 'object') {
        let detailPEm = document.createElement('em');
        detailPEm.setAttribute('class', 'movie_info_title');
        detailPEm.textContent = name;
        detailP.appendChild(detailPEm);
        detailP.append(" : ");

        for (let index=0; index<values.length; index+=1) {
            let item = values[index]
            let detailA = document.createElement('a');
            detailA.setAttribute('class', 'movie_info_link');

            if (name=='导演' || name=='演员' || name=='编剧') {
                detailA.setAttribute('href', '/celebrity/' + item['id']);
            } else if (name=='类型') {
                detailA.setAttribute('href', '/category/' + item['id']);
            } else if (name=='地区') {
                detailA.setAttribute('href', '/area/' + item['id']);
            } else {
                detailA.setAttribute('href', '/404');
            }

            if (index == values.length-1) {
                detailA.textContent = item['name'] ;
            } else {
                detailA.textContent = item['name'] + ",";
            }

            detailP.appendChild(detailA);
        }

    } else if (typeof values == 'string') {
        let detailPEm = document.createElement('em');
        detailPEm.setAttribute('class', 'movie_info_title');
        detailPEm.textContent = name;
        detailP.appendChild(detailPEm);

        detailP.append(" : ");
        detailP.append(values);
    } else {

    }

//    detailP.textContent = values;
    return detailP
}

// ==========  电影播放页 ==========
function updateVideoPlayerTitle(movie) {
	let titleDiv = document.getElementById('title');
	titleDiv.setAttribute('style', 'text-align: center;');
	let hTitle = document.createElement('h');
	hTitle.textContent = movie['name'] + '(' + movie['year'] + ")"
	titleDiv.appendChild(hTitle);
}

function showMoviePage(movieTr) {
//    let movieName = movieTr.children[0].innerText
    let movieId = movieTr.getAttribute('id')
    console.log("Show the detail of movie id: " + movieId)
    window.location = "subject/" + movieId;
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