document.addEventListener('DOMContentLoaded', function () {
    var getInfoButton = document.getElementById("getInfoButton");
    if (getInfoButton) {
        getInfoButton.onclick = function () {
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
        }
    }

    var getHeatDictButton = document.getElementById("getHeatDictButton");
    if (getHeatDictButton) {
        getHeatDictButton.onclick = function () {
            var url = BASE_URL + "/getheatdict?"
                + "git_client=" + document.getElementById("git_client").value
                + "&token=" + document.getElementById("token").value
                + "&repo=" + document.getElementById("repo").value
                + "&owner=" + document.getElementById("owner").value
                + "&form_of_date=" + document.getElementById("formOfDate").value;
            getHeatDict(url);
        }
    }



    var getLoginButton = document.getElementById("loginButton");
    if (getLoginButton){
        getLoginButton.onclick = loginService
    }

});

var BASE_URL = "http://0.0.0.0:8000";

function requestGet(url, successCallBack, errorCallBack) {

    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.send();
    xhr.onload = function () {
        var data = {
            body: JSON.parse(xhr.responseText),
            status: xhr.status
        };
        if (xhr.status >= 400) {
            if (errorCallBack !== undefined) {
                errorCallBack(data);
            } else {
            }
        } else {
            if (successCallBack !== undefined) {
                successCallBack(data);
            } else {
            }
        }
    };
}

function requestPost(url, data, successCallBack, errorCallBack) {

    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.send(JSON.stringify(data));
    xhr.onload = function () {
        var data = {
            body: JSON.parse(xhr.responseText),
            status: xhr.status
        }
        if (xhr.status >= 400) {
            if (errorCallBack !== undefined) {
                errorCallBack(data);
            } else {
            }
        } else {
            if (successCallBack !== undefined) {
                successCallBack(data);
            } else {
            }
        }
    };
}

function getRepoData(url) {
    requestGet(url, function (response) {
        document.getElementById("response").innerText = JSON.stringify(response.body);
    });
}

function getHeatDict(url) {
    requestGet(url, function (response) {
        document.getElementById("response").innerText = JSON.stringify(response.body);
    });
}

function loginService() {
    var data = {
        "username": document.getElementById("username").value,
        "password": document.getElementById("password").value
    }
    requestPost('/login', data,
        function (response) {
            window.location.href = '/'
        },
        function (badResponse) {
            document.getElementById('error').innerText = JSON.stringify(badResponse.body);
        }
    )
}
