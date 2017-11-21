import React from 'react'
import {
    Platform,
    StyleSheet,
    Text,
    View,
    TouchableHighlight,
    Button,
    Animated,
    Dimensions
} from 'react-native';

import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {refreshServerFiles} from '.././actions/index'
import * as Animatable from 'react-native-animatable';

let winSize = Dimensions.get('window');

class Controller extends React.Component {
    constructor() {
        super();
        this.state = {
            operationToggle: false,
            settingToggle: false,
        }
    }

    toggleOperation() {
        this.setState({
            operationToggle: !this.state.operationToggle,
        })
    }

    toggleSetting() {
        this.setState({
            settingToggle: !this.state.settingToggle,
        })
    }

    refreshServerFiles() {
        console.log('refreshServerFiles');
        fetch("http://10.145.241.99:3000/getAllFiles")
            .then((response) => response.json())
            .then((responseJSON) => {
                this.props.refreshServerFiles(responseJSON);
            })
            .catch((error) => {
                console.error(error);
            });

    }

    showAbout() {

    }


    render() {
        let operationWindow = this.state.operationToggle === true ? (
            <Animatable.View animation="fadeInUp" style={styles.operationToggle}>
                <View style={styles.toggleBtn}>
                    <Button
                        title="刷新"
                        onPress={this.refreshServerFiles.bind(this)}
                        style={styles.btnText}
                    />
                </View>
            </Animatable.View>) : null;
        let settingWindow = this.state.settingToggle === true ? (
            <Animatable.View animation="fadeInUp" style={styles.settingToggle}>
                <View style={styles.toggleBtn}>
                    <Button
                        title="关于"
                        onPress={this.showAbout.bind(this)}
                        style={styles.btnText}
                    />
                </View>
            </Animatable.View>) : null;
        return (
            <View style={styles.controller}>
                <View style={styles.bar}>
                    <View style={styles.btnContainer}>
                        <TouchableHighlight
                            underlayColor='white'
                            onPress={this.toggleOperation.bind(this)}
                        >
                            <Text style={styles.btnText}>操作</Text>
                        </TouchableHighlight>
                    </View>
                    {operationWindow}
                    <View style={styles.btnContainer}>
                        <TouchableHighlight
                            underlayColor='white'
                            onPress={this.toggleSetting.bind(this)}
                        >
                            <Text style={styles.btnText}>设定</Text>
                        </TouchableHighlight>
                    </View>
                    {settingWindow}
                </View>
            </View>
        )
    }
}

function mapStateToProps(state) {
    return {}
}

function matchDispatchToProps(dispatch) {
    return bindActionCreators({
        refreshServerFiles: refreshServerFiles
    }, dispatch)
}

const styles = StyleSheet.create({
    controller: {
        height: 80,
    },
    bar: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        margin: 10
    },
    btnContainer: {
        width: winSize.width / 2.2,
        padding: 10,
        borderWidth: 1,
        borderRadius: 5,
    },
    btnText: {
        textAlign: 'center',
        fontSize: 80 / winSize.scale,
        fontWeight: "bold"
    },
    operationToggle: {
        position: 'absolute',
        width: winSize.width / 2.2,
        borderWidth: 1,
        bottom: 58
    },
    settingToggle: {
        position: 'absolute',
        width: winSize.width / 2.2,
        borderWidth: 1,
        bottom: 58,
        right: 0
    },
    toggleBtn: {
        flex: 1,
        borderWidth: 1,
        borderBottomWidth: 0,
    }
});

export default connect(mapStateToProps, matchDispatchToProps)(Controller);