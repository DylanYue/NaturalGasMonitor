import {combineReducers} from 'redux';
import FetchServerFile from './reducer-fetch-server-files';
import FetchLocalFile from './reducer-fetch-local-files';
import FetchFiles from './reducer-fetch-files';

// const allReducers = combineReducers({
//     serverFiles: FetchServerFile,
//     localFiles: FetchLocalFile,
// });

const allReducers = combineReducers({
    files: FetchFiles,
});

export default allReducers;

