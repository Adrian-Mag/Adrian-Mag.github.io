(function () {
    "use strict";
    if (sessionStorage.getItem("sola-auth") !== "verified") {
        window.location.href = "sola-login.html";
    }
})();
