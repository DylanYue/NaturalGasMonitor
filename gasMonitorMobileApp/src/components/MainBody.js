import React from 'react';
import {
    Platform,
    StyleSheet,
    Text,
    View,
    ScrollView,
    Dimensions
} from 'react-native';

import MainBodyNavigator from './MainBodyNavigator';



class MainBody extends React.Component {
    componentWillMount() {

    }

    render() {
        return (
            <View style={styles.mainBody}>
                <MainBodyNavigator/>
            </View>
        )
    }
}

const styles = StyleSheet.create({});

export default MainBody;