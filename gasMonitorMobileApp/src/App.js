import React, {Component} from 'react';
import {Provider} from 'react-redux';
import {createStore} from 'redux';
import allReducers from './reducers/index';
import {
    Platform,
    StyleSheet,
    Text,
    View
} from 'react-native';
import RNFS from 'react-native-fs';

import Header from './components/Header';
import MainBodyNavigator from './components/MainBodyNavigator';
import Controller from './components/Controller';

const store = createStore(allReducers)
export default class App extends Component<{}> {
    render() {
        return (
            <Provider store={store}>
                <View style={styles.rootContainer}>
                    <MainBodyNavigator/>
                    <Controller/>
                </View>
            </Provider>
        );
    }
}


const styles = StyleSheet.create({
    rootContainer: {
        flex: 1,
        backgroundColor: '#F5FCFF'
    }
});
