/*
 * papers-crypto.js — client-side decryption for the in-preparation papers.
 *
 * Counterpart of tools/encrypt_papers.py. Files are AES-256-GCM with a
 * PBKDF2-HMAC-SHA256 key (600k iterations) derived from the access code:
 *
 *     magic "AMV1" (4) | salt (16) | nonce (12) | ciphertext+tag
 *
 * The access code is the actual decryption key — there is nothing to
 * bypass: without the code the repository and the served site contain
 * only ciphertext.
 *
 * Exposes window.PapersVault = { verifyCode, decryptToBlobUrl, hasSession,
 * storeCode, clearCode, requireSession }.
 */
(function () {
    "use strict";

    var ITERATIONS = 600000;
    var MAGIC = [0x41, 0x4D, 0x56, 0x31]; // "AMV1"
    var CANARY_URL = "../media/papers/vault-check.enc";
    var SESSION_KEY = "papers-code";

    function parseContainer(buf) {
        var bytes = new Uint8Array(buf);
        for (var i = 0; i < 4; i++) {
            if (bytes[i] !== MAGIC[i]) throw new Error("Not an encrypted papers file.");
        }
        return {
            salt: bytes.slice(4, 20),
            nonce: bytes.slice(20, 32),
            ct: bytes.slice(32)
        };
    }

    function deriveKey(code, salt) {
        var enc = new TextEncoder();
        return crypto.subtle.importKey("raw", enc.encode(code), "PBKDF2", false, ["deriveKey"])
            .then(function (base) {
                return crypto.subtle.deriveKey(
                    { name: "PBKDF2", salt: salt, iterations: ITERATIONS, hash: "SHA-256" },
                    base,
                    { name: "AES-GCM", length: 256 },
                    false,
                    ["decrypt"]
                );
            });
    }

    function decryptContainer(buf, code) {
        var c = parseContainer(buf);
        return deriveKey(code, c.salt).then(function (key) {
            return crypto.subtle.decrypt({ name: "AES-GCM", iv: c.nonce }, key, c.ct);
        });
    }

    /** Resolves true if the code decrypts the canary, false otherwise. */
    function verifyCode(code) {
        return fetch(CANARY_URL)
            .then(function (r) {
                if (!r.ok) throw new Error("canary missing");
                return r.arrayBuffer();
            })
            .then(function (buf) { return decryptContainer(buf, code); })
            .then(function () { return true; })
            .catch(function () { return false; });
    }

    /** Fetches an .enc file, decrypts it, returns a blob: URL for the PDF. */
    function decryptToBlobUrl(url, code) {
        return fetch(url)
            .then(function (r) {
                if (!r.ok) throw new Error("File not found: " + url);
                return r.arrayBuffer();
            })
            .then(function (buf) { return decryptContainer(buf, code); })
            .then(function (plain) {
                var blob = new Blob([plain], { type: "application/pdf" });
                return URL.createObjectURL(blob);
            });
    }

    function storeCode(code) {
        try { sessionStorage.setItem(SESSION_KEY, code); } catch (e) { /* ignore */ }
    }

    function getCode() {
        try { return sessionStorage.getItem(SESSION_KEY); } catch (e) { return null; }
    }

    function clearCode() {
        try { sessionStorage.removeItem(SESSION_KEY); } catch (e) { /* ignore */ }
    }

    function hasSession() { return !!getCode(); }

    /** Redirect to the login page when no code is stored. */
    function requireSession() {
        if (!hasSession()) window.location.href = "papers-login.html";
    }

    window.PapersVault = {
        verifyCode: verifyCode,
        decryptToBlobUrl: decryptToBlobUrl,
        storeCode: storeCode,
        getCode: getCode,
        clearCode: clearCode,
        hasSession: hasSession,
        requireSession: requireSession
    };
})();
