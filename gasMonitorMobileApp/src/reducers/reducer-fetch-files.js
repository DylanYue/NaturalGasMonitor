export default function (state = null, action) {
    let result = {};
    switch (action.type) {
        case "SERVER_FILE":
            result = {
                serverFiles: action.payload,
                localFiles: state.localFiles
            }
            return result;
            break;
        case "CLICK_DOWNLOAD":
            console.log("CLICK_DOWNLOAD", action.payload);
            return {
                serverFiles: action.payload.removed,
                localFiles: action.payload.added
            }
            break;
        case "LOCAL_FILE":
            result = {
                serverFiles: state.serverFiles,
                localFiles: action.payload,
            }
            return result;
            break;
        case "CLICK_REMOVE":
            return {
                serverFiles: action.payload.serverFiles,
                localFiles: action.payload.localFiles
            }
            break;
        case"REFRESH_FILES":
            return {
                serverFiles: action.payload,
                localFiles: state.localFiles
            }
            break;
    }
    return {
        serverFiles: [],
        localFiles: []
    };
}