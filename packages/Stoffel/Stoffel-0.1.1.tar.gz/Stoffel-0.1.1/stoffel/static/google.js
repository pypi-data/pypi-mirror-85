// The Browser API key obtained from the Google API Console.
// Replace with your own Browser API key, or your own key.
var developer_key = 'AIzaSyDNRPFphQ7TxAqm7IgLp_C8wrFQCYCTjww';

// The Client ID obtained from the Google API Console. Replace with your own Client ID.
var client_id = "823137768028-d165vk6p8c6jr469iqgo9dbp6o9jg421.apps.googleusercontent.com"

// Replace with your own project number from console.developers.google.com.
// See "Project number" under "IAM & Admin" > "Settings"
var appId = "823137768028";

// Scope to use to access user's Drive items.
var scope = ['https://www.googleapis.com/auth/drive.file'];

var pickerApiLoaded = false;
var oauthToken;
window.connection_id = "";

function onApiLoad(connection_id) {
    window.connection_id = connection_id.replace("button_", ""); 
    gapi.load('auth', {'callback':onAuthApiLoad});
    gapi.load('picker');
}
function onAuthApiLoad() {
    window.gapi.auth.authorize({
        'client_id': client_id,
        'scope' : scope
    }, handleAuthResult);
}

function handleAuthResult(authResult) {
    if (authResult && !authResult.error) {
        oauthtoken = authResult.access_token;
        createPicker();
    }

}
// function to create the Picker
function createPicker() {
            
    // we cab enable/disable picker's features by adding IE '.enableFeature(google.picker.Feature.MULTISELECT_ENABLED)'
    // picker class documentation available here: https://developers.google.com/picker/docs/reference#Feature
    var picker = new google.picker.PickerBuilder();

    picker.addView(new google.picker.DocsView())
        .setOAuthToken(oauthtoken)
        .setDeveloperKey(developer_key)
        .setCallback(pickerCallback) // designate a callback function
        .build()
        .setVisible(true);            
}

function pickerCallback(data) {
    if (data.action == google.picker.Action.PICKED) {
        var fileId = data.docs[0].id;
        $("input[name='" + window.connection_id + "']").val(fileId)
    }
}