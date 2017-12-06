import React, {Component} from 'react';
import {Provider} from 'react-redux';
import {createStore} from 'redux';
import allReducers from './reducers/index';
import {
    Platform,
    StyleSheet,
    Button,
    Text,
    View
} from 'react-native';
import MainBodyNavigator from './components/MainBodyNavigator';
import Controller from './components/Controller';
import RNFS from 'react-native-fs';
import {ANDROID_STORAGE_PATH} from './config/config'

var wifi = require('react-native-android-wifi');
const store = createStore(allReducers);

export default class App extends Component<{}> {
    constructor() {
        super();
        this.state = {
            isWifiEnabled: false,
            isWifiConnected: false,
            ip: "1111"
        }
    }

    componentWillMount() {
        RNFS.exists(ANDROID_STORAGE_PATH).then((isExist) => {
            console.log(ANDROID_STORAGE_PATH, isExist);
            if (!isExist) {
                RNFS.mkdir(ANDROID_STORAGE_PATH).then((result) => {
                    console.log('mkdir', result);
                }).catch((err) => {
                    console.log('mkdir', err)
                })
            }
        }).catch((err) => {
            console.log(err);
        });
    }


    componentDidMount() {
        console.log('did mount')
        wifi.isEnabled((isEnabled) => {
            if (isEnabled) this.setState({isWifiEnabled: true,})
        });
        wifi.connectionStatus((isConnected) => {
            if (isConnected) this.setState({isWifiConnected: true,})
        });
        wifi.getIP((ip) => {
            this.setState({ip: ip})
        })
    }

    enableWifi() {
        wifi.setEnabled(true);
        this.setState({isWifiEnabled: true,});
    }

    render() {
        let mainBody;
        const WifiEnableWarning = (
            <View style={styles.mainBody}>
                <Text style={styles.warningTxt}>请点击连接，打开WIFI</Text>
                <Button
                    title='连接'
                    onPress={this.enableWifi.bind(this)}
                />
            </View>
        )
        const WifiConnectionWarning = (
            <View style={styles.mainBody}>
                <Text style={styles.warningTxt}>请链接WIFI：RA_PI</Text>
            </View>
        )
        if (!this.state.isWifiEnabled) {
            mainBody = WifiEnableWarning
        } else if (!this.state.isWifiConnected) {
            mainBody = WifiConnectionWarning
        } else {
            mainBody = <MainBodyNavigator/>
        }

        return (
            <Provider store={store}>
                <View style={styles.rootContainer}>
                    {mainBody}
                    <Text>{this.state.ip}</Text>
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
    },
    mainBody: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center'
    },
    warningTxt: {
        fontWeight: '500',
        fontSize: 30,
        color: 'red'
    }


});
