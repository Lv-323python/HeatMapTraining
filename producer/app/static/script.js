document.addEventListener('DOMContentLoaded', function () {

    document.getElementById("getInfoButton").onclick = function () {
        var url = BASE_URL + "/getinfo?"
                + "git_client=" + document.getElementById("git_client").value
                + "&token=" + document.getElementById("token").value
                + "&version=" + document.getElementById("version").value
                + "&repo=" + document.getElementById("repo").value
                + "&owner=" + document.getElementById("owner").value
                + "&hash=" + document.getElementById("hash").value
                + "&branch=" + document.getElementById("branch").value
                + "&action=" + document.getElementById("action").value;
        getRepoData(url);
    };

});

var BASE_URL = "http://0.0.0.0:8000";

function requestGet(url, successCallBack, errorCallBack) {

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.send();
    xhr.onload = function () {
        var data = {
            body: Object.assign({}, JSON.parse(xhr.responseText)),
            status: xhr.status
        };
        if (xhr.status >= 400) {
            if (errorCallBack !== undefined) {
                errorCallBack(data);
            } else {
                console.log(xhr);
            }
        } else {
            if (successCallBack !== undefined) {
                successCallBack(data);
            } else {
                console.log(xhr);
            }
        }
    };
}

function requestPost(url, data, successCallBack, errorCallBack) {

    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.send(data);
    xhr.onload = function () {
        var data = {
            body: Object.assign({}, JSON.parse(xhr.responseText)),
            status: xhr.status
        }
        if (xhr.status >= 400) {
            if (errorCallBack !== undefined) {
                errorCallBack(data);
            } else {
                console.log(xhr);
            }
        } else {
            if (successCallBack !== undefined) {
                successCallBack(data);
            } else {
                console.log(xhr);
            }
        }
    };
}

function getRepoData(url) {
    requestGet(url, function (respons) {
        document.getElementById("response").innerText = JSON.stringify(respons.body);

    });
}
