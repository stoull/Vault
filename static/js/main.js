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
        	console.log(xmlHttp.responseText);
            drawRow(xmlHttp.responseText)
        // else
            // alert("错误：" + xmlHttp.readyState)
    }
    xmlHttp.open("GET", movie_json_url, true); // true for asynchronous 
    xmlHttp.send(null);
}

function drawRow(rowData) {
    var row = $("<tr />")
    $("#Database_tables").append(row); //this will append tr element to table... keep its reference for a while since we will add cels into it
    row.append($("<td>" + rowData.id + "</td>"));
    row.append($("<td>" + rowData.Name + "</td>"));
    row.append($("<td>" + rowData.Phone1 + "</td>"));
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