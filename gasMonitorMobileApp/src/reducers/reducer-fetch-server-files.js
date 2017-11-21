export default function (state = null, action) {
    console.log("state is: ", state);
    console.log("action is: ", action.type);
    console.log("payload is: ", action.payload);
    switch (action.type) {
        case "SERVER_FILE":
            return action.payload;
            break;
        case "CLICK_DOWNLOAD":
            return action.payload;
            break;
    }
    return state;
}