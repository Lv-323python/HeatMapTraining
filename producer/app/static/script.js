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

    var saveUserRepoInfoButton = document.getElementById("saveUserRepoInfo");
    if (saveUserRepoInfoButton){
        saveUserRepoInfoButton.onclick = saveUserRepoInfo;
    }

    var addNewRepoButton = document.getElementById("addNewRepoButton");
    if (addNewRepoButton){
        addNewRepoButton.onclick = addNewRepo;
    }

    getUserRequests();

});

var BASE_URL = "";

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
        console.log(data)
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
function requestDelete(url, successCallBack, errorCallBack) {

    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", url);
    xhr.send();
    xhr.onload = function () {
        var data = {
            body: JSON.parse(xhr.responseText),
            status: xhr.status
        }
        console.log(data)
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
        var data = response.body;
        plotHeatMap(data)
    });
}

function plotHeatMap(rawData){
    console.log("enter")
    console.log(typeof(rawData))
    console.log(typeof(rawData.x))
    console.log(rawData.y)
    console.log(rawData.z)

     var colorscaleValue = [
      [0, '#ebedf0'],
      [0.25, '#c6e48b'],
      [0.5, '#7bc96f'],
      [0.75, '#239a3b'],
      [1, '#196127']

    ];
    var data2 = [
      {
        z: rawData.z,
        x: rawData.x,
        y: rawData.y,
        xgap :	1,
        ygap :	1,
        type: 'heatmap',
        colorscale: colorscaleValue
      }
    ];
    document.getElementById("response").innerText = "";
    Plotly.newPlot('response', data2);
    console.log("exit")
}

function saveUserRepoInfo() {
    var data = {
        "git_client": document.getElementById("git_client").value,
        "version": document.getElementById("version").value,
        "repo": document.getElementById("repo").value,
        "owner": document.getElementById("owner").value,
        "token": document.getElementById("token").value,
        "hash": document.getElementById("hash").value,
        "branch": document.getElementById("branch").value,
        "action": document.getElementById("action").value,
    }
    requestPost('/user/requests', data,
        function (response) {
            console.log(response.body);
            var body = document.getElementById("repoValues");
            body.style.display = "none";
            getUserRequests();
        },
        function (badResponse) {
//            document.getElementById('error').innerText = JSON.stringify(badResponse.body);
        }
    )
}


function getUserRequests(){
    requestGet('/user/requests',
        function (response) {
            createTable(response.body);
        },
        function (badResponse) {
//            document.getElementById('error').innerText = JSON.stringify(badResponse.body);
        }
    )

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

function createTable(data){
    var table = document.getElementById("myTableTBody");
    while (table.firstChild) {
        table.removeChild(table.firstChild);
    }
    var ui_requests = ['git_client', 'version', 'repo', 'owner', 'token', 'hash', 'branch',
                       'action']
    for (i = 0; i < data.length; i++){

        var row = document.createElement("TR");
        var row_id = "row_" + data[i]["id"];
        row.setAttribute("id", row_id);
        table.appendChild(row);

        for(y = 0; y < ui_requests.length; y++){
            var td = document.createElement("TD");
            var td_data = document.createTextNode(data[i][ui_requests[y]]);
            td.appendChild(td_data);
            document.getElementById(row_id).appendChild(td);
        }

        //add edit button
        var td = document.createElement("TD");
        var button = document.createElement('INPUT')
        button.type = "button";
        button.value = 'Edit';
        button.class = 'editButton'
        button.setAttribute("onclick", 'editRepoInfo(' + data[i]["id"] + ')');
        td.appendChild(button);
        document.getElementById(row_id).appendChild(td);

        //add delete button
        var td = document.createElement("TD");
        var button = document.createElement('INPUT')
        button.type = "button";
        button.value = 'Delete';
        button.class = 'deleteButton'
        button.setAttribute("onclick", 'deleteRepoInfo(' + data[i]["id"] + ')');
        td.appendChild(button);

        //add row
        document.getElementById(row_id).appendChild(td);
   }
}

function addNewRepo(){
    var body = document.getElementById("repoValues");
    body.style.display = "block";
}

function deleteRepoInfo(id){
    var url =  '/table/' + id;
    requestDelete(url,
        function (response) {
            getUserRequests();
        },
        function (badResponse) {
//            document.getElementById('error').innerText = JSON.stringify(badResponse.body);
        }
    )
}
