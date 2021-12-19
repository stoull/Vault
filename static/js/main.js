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
    }
    xmlHttp.open("GET", movie_json_url, true); // true for asynchronous 
    xmlHttp.send(null);
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