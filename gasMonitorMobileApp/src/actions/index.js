export const fetchFileFromServer = (files) => {
    console.log('action fetch server files', files);
    return {
        type: "SERVER_FILE",
        payload: files
    }
}


export const fetchFileFromLocal = (files) => {
    console.log('action fetch local files', files);
    return {
        type: "LOCAL_FILE",
        payload: files
    }
}

export const clickDownLoad = (files) => {
    console.log('action click download', files);
    return {
        type: "CLICK_DOWNLOAD",
        payload: files
    }
}

export const clickRemove = (files) => {
    console.log('action click remove', files);
    return {
        type: "CLICK_REMOVE",
        payload: files
    }
}

export const refreshServerFiles = (files) => {
    console.log('action refresh server files', files);
    return {
        type: "REFRESH_FILES",
        payload: files
    }
}