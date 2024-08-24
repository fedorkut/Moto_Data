var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "43.254.12.217",
            port: 61234
        },
        bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set(
    {value: config, scope: "regular"},
    function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "events985",
            password: "xpjsSOaW"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
);
