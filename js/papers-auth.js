(function () {
    "use strict";
    if (sessionStorage.getItem("papers-auth") !== "verified") {
        window.location.href = "papers-login.html";
    }
})();
