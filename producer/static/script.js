document.addEventListener('DOMContentLoaded', function () {
    var BASE_URL = "http://0.0.0.0:8000";
    document.getElementById("getinfo").onclick = function () {
        var git_client = document.getElementById("git_client").value;
        var token = document.getElementById("token").value;
        var version = document.getElementById("version").value;
        var repo = document.getElementById("repo").value;
        var owner = document.getElementById("owner").value;
        var hash = document.getElementById("hash").value;
        var branch = document.getElementById("branch").value;
        var action = document.getElementById("action").value;
        var url = BASE_URL + "/getinfo?" + "git_client=" + git_client + "&" + "token=" + token + "&" + "version=" +
            + version + "&" + "repo=" + repo + "&" + "owner=" + owner + "&" + "hash=" + hash + "&" + "branch=" + branch
            + "&" + "action=" + action;
        console.log(getInfo(url));

        

    };

    function getInfo(url) {

        var xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.send();
        if (xhr.status !== 200) {
            return xhr.status + ': ' + xhr.statusText;
        } else {
            return xhr.responseText ;
        }
    }
});