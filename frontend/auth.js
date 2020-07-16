function getUser(){
    const token = "Bearer " + localStorage.token
    return $.ajax({
        url: 'https://dev-will.auth0.com/userinfo',
        type: "GET",
        headers: {
            'Authorization': token
        },
        success: (response) => {
            // console.log(response)
            return response
        },
        error: (error) => {
            login()
        }
    });
}

function logout(webAuth){
    localStorage.clear()
    console.log(localStorage)
    webAuth.logout({
        returnTo: 'http://127.0.0.1:5500/frontend/index.html',
        client_id: 'x7YM3jmiJVLNLDJSIccy1kw5RKdWC6AH'
    });
}

function login(webAuth){
    webAuth.authorize({
    });
}

// function login(webAuth, redirectUri){
//     webAuth.authorize({redirectUri
//     });
// }

function isExpired(token){
    console.log(token)
}