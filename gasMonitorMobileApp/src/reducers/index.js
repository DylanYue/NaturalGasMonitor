import {combineReducers} from 'redux';

import FetchFiles from './reducer-fetch-files';

const allReducers = combineReducers({
    files: FetchFiles,
});

export default allReducers;

