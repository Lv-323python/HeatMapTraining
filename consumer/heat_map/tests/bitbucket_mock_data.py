# data to use in mock response to test bitbucket
REPO_DATA = {
    "scm": "git",
    "website": "",
    "has_wiki": False,
    "name": "PublicBitbucketRepo",
    "links": {"watchers": {
        "href":
            "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/watchers"},
        "branches": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/refs/branches"},
        "tags": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/refs/tags"},
        "commits": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commits"},
        "clone": [{
            "href": "https://bitbucket.org/partsey/publicbitbucketrepo.git",
            "name": "https"},
            {
                "href": "git@bitbucket.org:partsey/publicbitbucketrepo.git",
                "name": "ssh"}],
        "self": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
        "source": {
            "href":
                "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/src"},
        "html": {
            "href":
                "https://bitbucket.org/partsey/publicbitbucketrepo"},
        "avatar": {
            "href":
                "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"},
        "hooks": {
            "href":
                "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/hooks"},
        "forks": {
            "href":
                "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/forks"},
        "downloads": {
            "href":
                "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/downloads"},
        "pullrequests": {
            "href":
                "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/pullrequests"}},
    "fork_policy": "allow_forks",
    "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}",
    "language": "",
    "created_on": "2018-06-28T15:29:14.763457+00:00",
    "mainbranch": {"type": "branch", "name": "master"},
    "full_name": "partsey/publicbitbucketrepo",
    "has_issues": False,
    "owner": {"username": "partsey",
              "display_name": "Руслан Парцей",
              "account_id": "5b346ed3f2886739ae9d985a",
              "links": {"self": {"href": "https://api.bitbucket.org/2.0/users/partsey"},
                        "html": {"href": "https://bitbucket.org/partsey/"},
                        "avatar": {"href": "https://bitbucket.org/account/partsey/avatar/"}},
              "type": "user",
              "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"},
    "updated_on": "2018-07-23T07:48:28.628160+00:00",
    "size": 163369,
    "type": "repository",
    "slug": "publicbitbucketrepo",
    "is_private": False,
    "description": ""
}

COMMITS_DATA = {
    "pagelen": 30, "value"
                   "s": [{"hash": "ad28081b8f17286689d1fef7efaad33dfcd6c4f3", "repository": {
        "links": {"self": {
            "href":
                "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
            "html": {
                "href":
                    "https://bitbucket.org/partsey/publicbitbucketrepo"}, "avatar": {
                "href":
                    "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
        "type":
            "repository", "name": "PublicBitbucketRepo", "full_name": "partsey/publicbitbucketrepo",
        "uuid":
            "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"}, "links": {
        "self": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/ad28081b8f17286689d1fef7efaad33dfcd6c4f3"},
        "comments": {
            "href":
                "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/ad28081b8f17286689d1fef7efaad33dfcd6c4f3/comments"},
        "patch": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/ad28081b8f17286689d1fef7efaad33dfcd6c4f3"},
        "html": {
            "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/ad28081b8f17286689d1fef7efaad33dfcd6c4f3"},
        "diff": {
            "href":
                "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/ad28081b8f17286689d1fef7efaad33dfcd6c4f3"},
        "approve": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/ad28081b8f17286689d1fef7efaad33dfcd6c4f3/approve"},
        "statuses": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/ad28081b8f17286689d1fef7efaad33dfcd6c4f3/statuses"}},
                          "author": {
                              "raw": "fake_user <user@example.com>",
                              "type": "author"},
                          "summary": {
                              "raw":
                                  "added file.txt\n",
                              "markup": "markdown",
                              "html": "<p>added file.txt</p>",
                              "type": "rendered"},
                          "parents": [
                              {
                                  "hash":
                                      "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6",
                                  "type": "commit",
                                  "links": {"self": {
                                      "href":
                                          "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                      "html": {
                                          "href":
                                              "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}}}],
                          "date":
                              "2018-07-23T07:48:07+00:00",
                          "message": "added file.txt\n",
                          "type":
                              "commit"}, {
                             "hash": "35a363addc596e1f3a0580d3dec1b78689be991d",
                             "repository": {
                                 "links": {
                                     "self": {
                                         "href":
                                             "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                     "html":
                                         {
                                             "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                     "avatar": {
                                         "href":
                                             "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                 "type":
                                     "repository",
                                 "name":
                                     "PublicBitbucketRepo",
                                 "full_name":
                                     "partsey/publicbitbucketrepo",
                                 "uuid":
                                     "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                             "links": {"self": {
                                 "href":
                                     "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d"},
                                 "comments":
                                     {
                                         "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/comments"},
                                 "html":
                                     {
                                         "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/35a363addc596e1f3a0580d3dec1b78689be991d"},
                                 "diff":
                                     {
                                         "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/35a363addc596e1f3a0580d3dec1b78689be991d"},
                                 "approve": {
                                     "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/approve"},
                                 "statuses": {
                                     "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/statuses"}},
                             "author": {"raw": "Partsey <partsey2412@gmail.com>",
                                        "type": "author", "user": {"username": "partsey",
                                                                   "display_name": "Руслан Парцей",
                                                                   "account_id": "5b346ed3f2886739ae9d985a",
                                                                   "links": {"self": {
                                                                       "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                       "html": {
                                                                           "href": "https://bitbucket.org/partsey/"},
                                                                       "avatar": {
                                                                           "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                   "type": "user",
                                                                   "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                             "summary": {"raw": "Merge branch 'beautiful-feature'\n",
                                         "markup": "markdown",
                                         "html": "<p>Merge branch 'beautiful-feature'</p>",
                                         "type": "rendered"}, "parents": [
            {"hash": "967449717d302d6f20d3c800f9964fc467aa8dc5", "type": "commit", "links": {"self": {
                "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5"},
                "html": {
                    "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/967449717d302d6f20d3c800f9964fc467aa8dc5"}}},
            {"hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6", "type": "commit", "links": {"self": {
                "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                "html": {
                    "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}}}],
                             "date": "2018-07-16T11:02:41+00:00",
                             "message": "Merge branch 'beautiful-feature'\n",
                             "type": "commit"},
                         {"hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6", "repository": {"links": {
                             "self": {
                                 "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                             "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                             "avatar": {
                                 "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                             "type": "repository",
                             "name": "PublicBitbucketRepo",
                             "full_name": "partsey/publicbitbucketrepo",
                             "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                          "links": {"self": {
                              "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                              "comments": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/comments"},
                              "patch": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                              "html": {
                                  "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                              "diff": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                              "approve": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/approve"},
                              "statuses": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/statuses"}},
                          "author": {"raw": "Partsey <partsey2412@gmail.com>", "type": "author",
                                     "user": {"username": "partsey", "display_name": "Руслан Парцей",
                                              "account_id": "5b346ed3f2886739ae9d985a", "links": {"self": {
                                             "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                             "html": {
                                                 "href": "https://bitbucket.org/partsey/"},
                                             "avatar": {
                                                 "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                              "type": "user",
                                              "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                          "summary": {"raw": "created temp2.txt\n",
                                      "markup": "markdown",
                                      "html": "<p>created temp2.txt</p>",
                                      "type": "rendered"}, "parents": [
                             {"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6",
                              "type": "commit",
                              "links": {"self": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                  "html": {
                                      "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"}}}],
                          "date": "2018-07-16T11:01:02+00:00", "message": "created temp2.txt\n",
                          "type": "commit"}, {"hash": "967449717d302d6f20d3c800f9964fc467aa8dc5",
                                              "repository": {"links": {"self": {
                                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                  "html": {
                                                      "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                  "avatar": {
                                                      "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                  "type": "repository",
                                                  "name": "PublicBitbucketRepo",
                                                  "full_name": "partsey/publicbitbucketrepo",
                                                  "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                              "links": {"self": {
                                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5"},
                                                  "comments": {
                                                      "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5/comments"},
                                                  "patch": {
                                                      "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/967449717d302d6f20d3c800f9964fc467aa8dc5"},
                                                  "html": {
                                                      "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/967449717d302d6f20d3c800f9964fc467aa8dc5"},
                                                  "diff": {
                                                      "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/967449717d302d6f20d3c800f9964fc467aa8dc5"},
                                                  "approve": {
                                                      "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5/approve"},
                                                  "statuses": {
                                                      "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5/statuses"}},
                                              "author": {"raw": "Partsey <partsey2412@gmail.com>",
                                                         "type": "author", "user": {"username": "partsey",
                                                                                    "display_name": "Руслан Парцей",
                                                                                    "account_id": "5b346ed3f2886739ae9d985a",
                                                                                    "links": {"self": {
                                                                                        "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                                        "html": {
                                                                                            "href": "https://bitbucket.org/partsey/"},
                                                                                        "avatar": {
                                                                                            "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                                    "type": "user",
                                                                                    "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                                              "summary": {"raw": "created temp1.txt\n",
                                                          "markup": "markdown",
                                                          "html": "<p>created temp1.txt</p>",
                                                          "type": "rendered"}, "parents": [
                {"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6",

                 "type": "commit", "links": {"self": {
                    "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                    "html": {
                        "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"}}}],
                                              "date": "2018-07-16T10:59:10+00:00",
                                              "message": "created temp1.txt\n", "type": "commit"},
                         {"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6", "repository": {"links": {
                             "self": {
                                 "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                             "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                             "avatar": {
                                 "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                             "type": "repository",
                             "name": "PublicBitbucketRepo",
                             "full_name": "partsey/publicbitbucketrepo",
                             "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                          "links": {"self": {
                              "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                              "comments": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/comments"},
                              "patch": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                              "html": {
                                  "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                              "diff": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                              "approve": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/approve"},
                              "statuses": {
                                  "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/statuses"}},
                          "author": {"raw": "Partsey <partsey2412@gmail.com>", "type": "author",
                                     "user": {"username": "partsey", "display_name": "Руслан Парцей",
                                              "account_id": "5b346ed3f2886739ae9d985a", "links": {"self": {
                                             "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                             "html": {
                                                 "href": "https://bitbucket.org/partsey/"},
                                             "avatar": {
                                                 "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                              "type": "user",
                                              "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                          "summary": {
                              "raw": "created temp.txt\n", "markup": "markdown",
                              "html": "<p>created temp.txt</p>", "type": "rendered"}, "parents": [
                             {
                                 "hash": "8333878971e78108e3a3fff76bd44ed308a5fada", "type": "commit",
                                 "links": {"self": {
                                     "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                     "html": {
                                         "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8333878971e78108e3a3fff76bd44ed308a5fada"}}}],
                          "date": "2018-07-16T10:56:15+00:00", "message": "created temp.txt\n",
                          "type": "commit"}, {
                             "hash": "8333878971e78108e3a3fff76bd44ed308a5fada",
                             "repository": {"links": {"self": {
                                 "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                 "html": {
                                     "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                 "avatar": {
                                     "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                 "type": "repository",
                                 "name": "PublicBitbucketRepo",
                                 "full_name": "partsey/publicbitbucketrepo",
                                 "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                             "links": {
                                 "self": {
                                     "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                 "comments": {
                                     "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/comments"},
                                 "patch": {
                                     "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                 "html": {
                                     "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                 "diff": {
                                     "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                 "approve": {
                                     "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/approve"},
                                 "statuses": {
                                     "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/statuses"}},
                             "author": {
                                 "raw": "Ruslan Partsey <partsey2412@gmail.com>",
                                 "type": "author", "user": {"username": "partsey",
                                                            "display_name": "Руслан Парцей",
                                                            "account_id": "5b346ed3f2886739ae9d985a",
                                                            "links": {"self": {
                                                                "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                "html": {
                                                                    "href": "https://bitbucket.org/partsey/"},
                                                                "avatar": {
                                                                    "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                            "type": "user",
                                                            "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                             "summary": {"raw": "initial commit + created  README.md\n",
                                         "markup": "markdown",
                                         "html": "<p>initial commit + created  README.md</p>",
                                         "type": "rendered"}, "parents": [],
                             "date": "2018-06-28T15:32:03+00:00",
                             "message": "initial commit + created  README.md\n",
                             "type": "commit"
                         }]}

BRANCHES_DATA = {"values": [{"name": "awesome-feature"}, {"name": "beautiful-feature"}, {"name": "master"}]}

COMMIT_BY_AWESOME_BRANCH = {"pagelen": 30, "values": [{"hash": "35a363addc596e1f3a0580d3dec1b78689be991d",
                                                       "repository": {"links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                           "avatar": {
                                                               "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                           "type": "repository",
                                                           "name": "PublicBitbucketRepo",
                                                           "full_name": "partsey/publicbitbucketrepo",
                                                           "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                                       "links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d"},
                                                           "comments": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/comments"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/35a363addc596e1f3a0580d3dec1b78689be991d"},
                                                           "diff": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/35a363addc596e1f3a0580d3dec1b78689be991d"},
                                                           "approve": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/approve"},
                                                           "statuses": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/statuses"}},
                                                       "author": {"raw": "Partsey <partsey2412@gmail.com>",
                                                                  "type": "author", "user": {"username": "partsey",
                                                                                             "display_name": "Руслан Парцей",
                                                                                             "account_id": "5b346ed3f2886739ae9d985a",
                                                                                             "links": {"self": {
                                                                                                 "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                                                 "html": {
                                                                                                     "href": "https://bitbucket.org/partsey/"},
                                                                                                 "avatar": {
                                                                                                     "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                                             "type": "user",
                                                                                             "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                                                       "summary": {"raw": "Merge branch 'beautiful-feature'\n",
                                                                   "markup": "markdown",
                                                                   "html": "<p>Merge branch 'beautiful-feature'</p>",
                                                                   "type": "rendered"}, "parents": [
        {"hash": "967449717d302d6f20d3c800f9964fc467aa8dc5", "type": "commit", "links": {"self": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5"},
            "html": {
                "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/967449717d302d6f20d3c800f9964fc467aa8dc5"}}},
        {"hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6", "type": "commit", "links": {"self": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
            "html": {
                "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}}}],
                                                       "date": "2018-07-16T11:02:41+00:00",
                                                       "message": "Merge branch 'beautiful-feature'\n",
                                                       "type": "commit"},
                                                      {"hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6",
                                                       "repository": {"links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                           "avatar": {
                                                               "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                           "type": "repository",
                                                           "name": "PublicBitbucketRepo",
                                                           "full_name": "partsey/publicbitbucketrepo",
                                                           "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                                       "links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                                           "comments": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/comments"},
                                                           "patch": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                                           "diff": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                                           "approve": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/approve"},
                                                           "statuses": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/statuses"}},
                                                       "author": {"raw": "Partsey <partsey2412@gmail.com>",
                                                                  "type": "author", "user": {"username": "partsey",
                                                                                             "display_name": "Руслан Парцей",
                                                                                             "account_id": "5b346ed3f2886739ae9d985a",
                                                                                             "links": {"self": {
                                                                                                 "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                                                 "html": {
                                                                                                     "href": "https://bitbucket.org/partsey/"},
                                                                                                 "avatar": {
                                                                                                     "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                                             "type": "user",
                                                                                             "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                                                       "summary": {"raw": "created temp2.txt\n", "markup": "markdown",
                                                                   "html": "<p>created temp2.txt</p>",
                                                                   "type": "rendered"}, "parents": [
                                                          {"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6",
                                                           "type": "commit", "links": {"self": {
                                                              "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                              "html": {
                                                                  "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"}}}],
                                                       "date": "2018-07-16T11:01:02+00:00",
                                                       "message": "created temp2.txt\n", "type": "commit"},
                                                      {"hash": "967449717d302d6f20d3c800f9964fc467aa8dc5",
                                                       "repository": {"links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                           "avatar": {
                                                               "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                           "type": "repository",
                                                           "name": "PublicBitbucketRepo",
                                                           "full_name": "partsey/publicbitbucketrepo",
                                                           "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                                       "links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5"},
                                                           "comments": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5/comments"},
                                                           "patch": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/967449717d302d6f20d3c800f9964fc467aa8dc5"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/967449717d302d6f20d3c800f9964fc467aa8dc5"},
                                                           "diff": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/967449717d302d6f20d3c800f9964fc467aa8dc5"},
                                                           "approve": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5/approve"},
                                                           "statuses": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5/statuses"}},
                                                       "author": {"raw": "Partsey <partsey2412@gmail.com>",
                                                                  "type": "author", "user": {"username": "partsey",
                                                                                             "display_name": "Руслан Парцей",
                                                                                             "account_id": "5b346ed3f2886739ae9d985a",
                                                                                             "links": {"self": {
                                                                                                 "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                                                 "html": {
                                                                                                     "href": "https://bitbucket.org/partsey/"},
                                                                                                 "avatar": {
                                                                                                     "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                                             "type": "user",
                                                                                             "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                                                       "summary": {"raw": "created temp1.txt\n", "markup": "markdown",
                                                                   "html": "<p>created temp1.txt</p>",
                                                                   "type": "rendered"}, "parents": [
                                                          {"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6",
                                                           "type": "commit", "links": {"self": {
                                                              "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                              "html": {
                                                                  "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"}}}],
                                                       "date": "2018-07-16T10:59:10+00:00",
                                                       "message": "created temp1.txt\n", "type": "commit"},
                                                      {"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6",
                                                       "repository": {"links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                           "avatar": {
                                                               "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                           "type": "repository",
                                                           "name": "PublicBitbucketRepo",
                                                           "full_name": "partsey/publicbitbucketrepo",
                                                           "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                                       "links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                           "comments": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/comments"},
                                                           "patch": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                           "diff": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                           "approve": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/approve"},
                                                           "statuses": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/statuses"}},
                                                       "author": {"raw": "Partsey <partsey2412@gmail.com>",
                                                                  "type": "author", "user": {"username": "partsey",
                                                                                             "display_name": "Руслан Парцей",
                                                                                             "account_id": "5b346ed3f2886739ae9d985a",
                                                                                             "links": {"self": {
                                                                                                 "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                                                 "html": {
                                                                                                     "href": "https://bitbucket.org/partsey/"},
                                                                                                 "avatar": {
                                                                                                     "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                                             "type": "user",
                                                                                             "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                                                       "summary": {"raw": "created temp.txt\n", "markup": "markdown",
                                                                   "html": "<p>created temp.txt</p>",
                                                                   "type": "rendered"}, "parents": [
                                                          {"hash": "8333878971e78108e3a3fff76bd44ed308a5fada",
                                                           "type": "commit", "links": {"self": {
                                                              "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                              "html": {
                                                                  "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8333878971e78108e3a3fff76bd44ed308a5fada"}}}],
                                                       "date": "2018-07-16T10:56:15+00:00",
                                                       "message": "created temp.txt\n", "type": "commit"},
                                                      {"hash": "8333878971e78108e3a3fff76bd44ed308a5fada",
                                                       "repository": {"links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                           "avatar": {
                                                               "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                           "type": "repository",
                                                           "name": "PublicBitbucketRepo",
                                                           "full_name": "partsey/publicbitbucketrepo",
                                                           "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                                       "links": {"self": {
                                                           "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                           "comments": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/comments"},
                                                           "patch": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                           "html": {
                                                               "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                           "diff": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                           "approve": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/approve"},
                                                           "statuses": {
                                                               "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/statuses"}},
                                                       "author": {"raw": "Ruslan Partsey <partsey2412@gmail.com>",
                                                                  "type": "author", "user": {"username": "partsey",
                                                                                             "display_name": "Руслан Парцей",
                                                                                             "account_id": "5b346ed3f2886739ae9d985a",
                                                                                             "links": {"self": {
                                                                                                 "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                                                 "html": {
                                                                                                     "href": "https://bitbucket.org/partsey/"},
                                                                                                 "avatar": {
                                                                                                     "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                                             "type": "user",
                                                                                             "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                                                       "summary": {"raw": "initial commit + created  README.md\n",
                                                                   "markup": "markdown",
                                                                   "html": "<p>initial commit + created  README.md</p>",
                                                                   "type": "rendered"}, "parents": [],
                                                       "date": "2018-06-28T15:32:03+00:00",
                                                       "message": "initial commit + created  README.md\n",
                                                       "type": "commit"}]}

COMMIT_BY_BEAUTIFUL_BRANCH = {"pagelen": 30, "values": [{"hash": "ad28081b8f17286689d1fef7efaad33dfcd6c4f3",
                                                         "repository": {"links": {"self": {
                                                             "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                                                  "html": {
                                                                                      "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                                                  "avatar": {
                                                                                      "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                                        "type": "repository",
                                                                        "name": "PublicBitbucketRepo",
                                                                        "full_name": "partsey/publicbitbucketrepo",
                                                                        "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                                         "links": {"self": {
                                                             "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/ad28081b8f17286689d1fef7efaad33dfcd6c4f3"},
                                                                   "comments": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/ad28081b8f17286689d1fef7efaad33dfcd6c4f3/comments"},
                                                                   "patch": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/ad28081b8f17286689d1fef7efaad33dfcd6c4f3"},
                                                                   "html": {
                                                                       "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/ad28081b8f17286689d1fef7efaad33dfcd6c4f3"},
                                                                   "diff": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/ad28081b8f17286689d1fef7efaad33dfcd6c4f3"},
                                                                   "approve": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/ad28081b8f17286689d1fef7efaad33dfcd6c4f3/approve"},
                                                                   "statuses": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/ad28081b8f17286689d1fef7efaad33dfcd6c4f3/statuses"}},
                                                         "author": {"raw": "fake_user <user@example.com>",
                                                                    "type": "author"},
                                                         "summary": {"raw": "added file.txt\n", "markup": "markdown",
                                                                     "html": "<p>added file.txt</p>",
                                                                     "type": "rendered"}, "parents": [
        {"hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6", "type": "commit", "links": {"self": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                                                                         "html": {
                                                                                             "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}}}],
                                                         "date": "2018-07-23T07:48:07+00:00",
                                                         "message": "added file.txt\n", "type": "commit"},
                                                        {"hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6",
                                                         "repository": {"links": {"self": {
                                                             "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                                                  "html": {
                                                                                      "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                                                  "avatar": {
                                                                                      "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                                        "type": "repository",
                                                                        "name": "PublicBitbucketRepo",
                                                                        "full_name": "partsey/publicbitbucketrepo",
                                                                        "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                                         "links": {"self": {
                                                             "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                                                   "comments": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/comments"},
                                                                   "patch": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                                                   "html": {
                                                                       "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                                                   "diff": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"},
                                                                   "approve": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/approve"},
                                                                   "statuses": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/statuses"}},
                                                         "author": {"raw": "Partsey <partsey2412@gmail.com>",
                                                                    "type": "author", "user": {"username": "partsey",
                                                                                               "display_name": "Руслан Парцей",
                                                                                               "account_id": "5b346ed3f2886739ae9d985a",
                                                                                               "links": {"self": {
                                                                                                   "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                                                         "html": {
                                                                                                             "href": "https://bitbucket.org/partsey/"},
                                                                                                         "avatar": {
                                                                                                             "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                                               "type": "user",
                                                                                               "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                                                         "summary": {"raw": "created temp2.txt\n", "markup": "markdown",
                                                                     "html": "<p>created temp2.txt</p>",
                                                                     "type": "rendered"}, "parents": [
                                                            {"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6",
                                                             "type": "commit", "links": {"self": {
                                                                "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                                                         "html": {
                                                                                             "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"}}}],
                                                         "date": "2018-07-16T11:01:02+00:00",
                                                         "message": "created temp2.txt\n", "type": "commit"},
                                                        {"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6",
                                                         "repository": {"links": {"self": {
                                                             "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                                                  "html": {
                                                                                      "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                                                  "avatar": {
                                                                                      "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                                        "type": "repository",
                                                                        "name": "PublicBitbucketRepo",
                                                                        "full_name": "partsey/publicbitbucketrepo",
                                                                        "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                                         "links": {"self": {
                                                             "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                                   "comments": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/comments"},
                                                                   "patch": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                                   "html": {
                                                                       "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                                   "diff": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/992572f32da2743ad8e86ad1cc7338284c3792c6"},
                                                                   "approve": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/approve"},
                                                                   "statuses": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/statuses"}},
                                                         "author": {"raw": "Partsey <partsey2412@gmail.com>",
                                                                    "type": "author", "user": {"username": "partsey",
                                                                                               "display_name": "Руслан Парцей",
                                                                                               "account_id": "5b346ed3f2886739ae9d985a",
                                                                                               "links": {"self": {
                                                                                                   "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                                                         "html": {
                                                                                                             "href": "https://bitbucket.org/partsey/"},
                                                                                                         "avatar": {
                                                                                                             "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                                               "type": "user",
                                                                                               "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                                                         "summary": {"raw": "created temp.txt\n", "markup": "markdown",
                                                                     "html": "<p>created temp.txt</p>",
                                                                     "type": "rendered"}, "parents": [
                                                            {"hash": "8333878971e78108e3a3fff76bd44ed308a5fada",
                                                             "type": "commit", "links": {"self": {
                                                                "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                                                         "html": {
                                                                                             "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8333878971e78108e3a3fff76bd44ed308a5fada"}}}],
                                                         "date": "2018-07-16T10:56:15+00:00",
                                                         "message": "created temp.txt\n", "type": "commit"},
                                                        {"hash": "8333878971e78108e3a3fff76bd44ed308a5fada",
                                                         "repository": {"links": {"self": {
                                                             "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"},
                                                                                  "html": {
                                                                                      "href": "https://bitbucket.org/partsey/publicbitbucketrepo"},
                                                                                  "avatar": {
                                                                                      "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}},
                                                                        "type": "repository",
                                                                        "name": "PublicBitbucketRepo",
                                                                        "full_name": "partsey/publicbitbucketrepo",
                                                                        "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"},
                                                         "links": {"self": {
                                                             "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                                   "comments": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/comments"},
                                                                   "patch": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                                   "html": {
                                                                       "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                                   "diff": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/8333878971e78108e3a3fff76bd44ed308a5fada"},
                                                                   "approve": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/approve"},
                                                                   "statuses": {
                                                                       "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/statuses"}},
                                                         "author": {"raw": "Ruslan Partsey <partsey2412@gmail.com>",
                                                                    "type": "author", "user": {"username": "partsey",
                                                                                               "display_name": "Руслан Парцей",
                                                                                               "account_id": "5b346ed3f2886739ae9d985a",
                                                                                               "links": {"self": {
                                                                                                   "href": "https://api.bitbucket.org/2.0/users/partsey"},
                                                                                                         "html": {
                                                                                                             "href": "https://bitbucket.org/partsey/"},
                                                                                                         "avatar": {
                                                                                                             "href": "https://bitbucket.org/account/partsey/avatar/"}},
                                                                                               "type": "user",
                                                                                               "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}},
                                                         "summary": {"raw": "initial commit + created  README.md\n",
                                                                     "markup": "markdown",
                                                                     "html": "<p>initial commit + created  README.md</p>",
                                                                     "type": "rendered"}, "parents": [],
                                                         "date": "2018-06-28T15:32:03+00:00",
                                                         "message": "initial commit + created  README.md\n",
                                                         "type": "commit"}]}

COMMIT_BY_MASTER = {"pagelen": 30, "values": [{"hash": "35a363addc596e1f3a0580d3dec1b78689be991d", "repository": {"links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo"}, "avatar": {"href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}}, "type": "repository", "name": "PublicBitbucketRepo", "full_name": "partsey/publicbitbucketrepo", "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"}, "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d"}, "comments": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/comments"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/35a363addc596e1f3a0580d3dec1b78689be991d"}, "diff": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/35a363addc596e1f3a0580d3dec1b78689be991d"}, "approve": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/approve"}, "statuses": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/statuses"}}, "author": {"raw": "Partsey <partsey2412@gmail.com>", "type": "author", "user": {"username": "partsey", "display_name": "Руслан Парцей", "account_id": "5b346ed3f2886739ae9d985a", "links": {"self": {"href": "https://api.bitbucket.org/2.0/users/partsey"}, "html": {"href": "https://bitbucket.org/partsey/"}, "avatar": {"href": "https://bitbucket.org/account/partsey/avatar/"}}, "type": "user", "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}}, "summary": {"raw": "Merge branch 'beautiful-feature'\n", "markup": "markdown", "html": "<p>Merge branch 'beautiful-feature'</p>", "type": "rendered"}, "parents": [{"hash": "967449717d302d6f20d3c800f9964fc467aa8dc5", "type": "commit", "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/967449717d302d6f20d3c800f9964fc467aa8dc5"}}}, {"hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6", "type": "commit", "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}}}], "date": "2018-07-16T11:02:41+00:00", "message": "Merge branch 'beautiful-feature'\n", "type": "commit"}, {"hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6", "repository": {"links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo"}, "avatar": {"href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}}, "type": "repository", "name": "PublicBitbucketRepo", "full_name": "partsey/publicbitbucketrepo", "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"}, "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}, "comments": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/comments"}, "patch": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}, "diff": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"}, "approve": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/approve"}, "statuses": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6/statuses"}}, "author": {"raw": "Partsey <partsey2412@gmail.com>", "type": "author", "user": {"username": "partsey", "display_name": "Руслан Парцей", "account_id": "5b346ed3f2886739ae9d985a", "links": {"self": {"href": "https://api.bitbucket.org/2.0/users/partsey"}, "html": {"href": "https://bitbucket.org/partsey/"}, "avatar": {"href": "https://bitbucket.org/account/partsey/avatar/"}}, "type": "user", "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}}, "summary": {"raw": "created temp2.txt\n", "markup": "markdown", "html": "<p>created temp2.txt</p>", "type": "rendered"}, "parents": [{"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6", "type": "commit", "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"}}}], "date": "2018-07-16T11:01:02+00:00", "message": "created temp2.txt\n", "type": "commit"}, {"hash": "967449717d302d6f20d3c800f9964fc467aa8dc5", "repository": {"links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo"}, "avatar": {"href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}}, "type": "repository", "name": "PublicBitbucketRepo", "full_name": "partsey/publicbitbucketrepo", "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"}, "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5"}, "comments": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5/comments"}, "patch": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/967449717d302d6f20d3c800f9964fc467aa8dc5"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/967449717d302d6f20d3c800f9964fc467aa8dc5"}, "diff": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/967449717d302d6f20d3c800f9964fc467aa8dc5"}, "approve": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5/approve"}, "statuses": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5/statuses"}}, "author": {"raw": "Partsey <partsey2412@gmail.com>", "type": "author", "user": {"username": "partsey", "display_name": "Руслан Парцей", "account_id": "5b346ed3f2886739ae9d985a", "links": {"self": {"href": "https://api.bitbucket.org/2.0/users/partsey"}, "html": {"href": "https://bitbucket.org/partsey/"}, "avatar": {"href": "https://bitbucket.org/account/partsey/avatar/"}}, "type": "user", "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}}, "summary": {"raw": "created temp1.txt\n", "markup": "markdown", "html": "<p>created temp1.txt</p>", "type": "rendered"}, "parents": [{"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6", "type": "commit", "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"}}}], "date": "2018-07-16T10:59:10+00:00", "message": "created temp1.txt\n", "type": "commit"}, {"hash": "992572f32da2743ad8e86ad1cc7338284c3792c6", "repository": {"links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo"}, "avatar": {"href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}}, "type": "repository", "name": "PublicBitbucketRepo", "full_name": "partsey/publicbitbucketrepo", "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"}, "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6"}, "comments": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/comments"}, "patch": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/992572f32da2743ad8e86ad1cc7338284c3792c6"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/992572f32da2743ad8e86ad1cc7338284c3792c6"}, "diff": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/992572f32da2743ad8e86ad1cc7338284c3792c6"}, "approve": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/approve"}, "statuses": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/992572f32da2743ad8e86ad1cc7338284c3792c6/statuses"}}, "author": {"raw": "Partsey <partsey2412@gmail.com>", "type": "author", "user": {"username": "partsey", "display_name": "Руслан Парцей", "account_id": "5b346ed3f2886739ae9d985a", "links": {"self": {"href": "https://api.bitbucket.org/2.0/users/partsey"}, "html": {"href": "https://bitbucket.org/partsey/"}, "avatar": {"href": "https://bitbucket.org/account/partsey/avatar/"}}, "type": "user", "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}}, "summary": {"raw": "created temp.txt\n", "markup": "markdown", "html": "<p>created temp.txt</p>", "type": "rendered"}, "parents": [{"hash": "8333878971e78108e3a3fff76bd44ed308a5fada", "type": "commit", "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8333878971e78108e3a3fff76bd44ed308a5fada"}}}], "date": "2018-07-16T10:56:15+00:00", "message": "created temp.txt\n", "type": "commit"}, {"hash": "8333878971e78108e3a3fff76bd44ed308a5fada", "repository": {"links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo"}, "avatar": {"href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"}}, "type": "repository", "name": "PublicBitbucketRepo", "full_name": "partsey/publicbitbucketrepo", "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"}, "links": {"self": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada"}, "comments": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/comments"}, "patch": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/patch/8333878971e78108e3a3fff76bd44ed308a5fada"}, "html": {"href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8333878971e78108e3a3fff76bd44ed308a5fada"}, "diff": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/8333878971e78108e3a3fff76bd44ed308a5fada"}, "approve": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/approve"}, "statuses": {"href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8333878971e78108e3a3fff76bd44ed308a5fada/statuses"}}, "author": {"raw": "Ruslan Partsey <partsey2412@gmail.com>", "type": "author", "user": {"username": "partsey", "display_name": "Руслан Парцей", "account_id": "5b346ed3f2886739ae9d985a", "links": {"self": {"href": "https://api.bitbucket.org/2.0/users/partsey"}, "html": {"href": "https://bitbucket.org/partsey/"}, "avatar": {"href": "https://bitbucket.org/account/partsey/avatar/"}}, "type": "user", "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"}}, "summary": {"raw": "initial commit + created  README.md\n", "markup": "markdown", "html": "<p>initial commit + created  README.md</p>", "type": "rendered"}, "parents": [], "date": "2018-06-28T15:32:03+00:00", "message": "initial commit + created  README.md\n", "type": "commit"}]}

COMMIT_BY_HASH_35a363={
    "hash": "35a363addc596e1f3a0580d3dec1b78689be991d",
    "repository": {
        "links": {
            "self": {
                "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo"
            },
            "html": {
                "href": "https://bitbucket.org/partsey/publicbitbucketrepo"
            },
            "avatar": {
                "href": "https://bytebucket.org/ravatar/%7Bbd061b16-a281-4368-bc45-c2f78f8eb63c%7D?ts=default"
            }
        },
        "type": "repository",
        "name": "PublicBitbucketRepo",
        "full_name": "partsey/publicbitbucketrepo",
        "uuid": "{bd061b16-a281-4368-bc45-c2f78f8eb63c}"
    },
    "links": {
        "self": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d"
        },
        "comments": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/comments"
        },
        "html": {
            "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/35a363addc596e1f3a0580d3dec1b78689be991d"
        },
        "diff": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/diff/35a363addc596e1f3a0580d3dec1b78689be991d"
        },
        "approve": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/approve"
        },
        "statuses": {
            "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/35a363addc596e1f3a0580d3dec1b78689be991d/statuses"
        }
    },
    "author": {
        "raw": "Partsey <partsey2412@gmail.com>",
        "user": {
            "username": "partsey",
            "display_name": "Руслан Парцей",
            "account_id": "5b346ed3f2886739ae9d985a",
            "links": {
                "self": {
                    "href": "https://api.bitbucket.org/2.0/users/partsey"
                },
                "html": {
                    "href": "https://bitbucket.org/partsey/"
                },
                "avatar": {
                    "href": "https://bitbucket.org/account/partsey/avatar/"
                }
            },
            "type": "user",
            "uuid": "{4783f390-7bac-4aaf-bb2e-9023cf44beb8}"
        }
    },
    "summary": {
        "raw": "Merge branch 'beautiful-feature'\n",
        "markup": "markdown",
        "html": "<p>Merge branch 'beautiful-feature'</p>",
        "type": "rendered"
    },
    "participants": [],
    "parents": [
        {
            "hash": "967449717d302d6f20d3c800f9964fc467aa8dc5",
            "type": "commit",
            "links": {
                "self": {
                    "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/967449717d302d6f20d3c800f9964fc467aa8dc5"
                },
                "html": {
                    "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/967449717d302d6f20d3c800f9964fc467aa8dc5"
                }
            }
        },
        {
            "hash": "8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6",
            "type": "commit",
            "links": {
                "self": {
                    "href": "https://api.bitbucket.org/2.0/repositories/partsey/publicbitbucketrepo/commit/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"
                },
                "html": {
                    "href": "https://bitbucket.org/partsey/publicbitbucketrepo/commits/8b4a937ad98639fa3231cfa4b29dd0e8b25a6dd6"
                }
            }
        }
    ],
    "date": "2018-07-16T11:02:41+00:00",
    "message": "Merge branch 'beautiful-feature'\n",
    "type": "commit"
}