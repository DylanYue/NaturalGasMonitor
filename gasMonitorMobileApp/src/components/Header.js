import React from 'react'
import {
    Platform,
    StyleSheet,
    Text,
    View,
    Dimensions
} from 'react-native';

let winSize = Dimensions.get('window');

class Header extends React.Component {
    render() {
        return (
            <View style={styles.header}>
                <View style={styles.heading}>
                    <Text style={styles.headingText}>设备文件管理</Text>
                </View>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    header: {
        height: 50
    },
    heading: {
        flex: 1,
        justifyContent: 'center',
        margin: 10,
        borderWidth: 1,
        borderRadius: 5
    },
    headingText: {
        textAlign: 'center',
        fontSize: 80 / winSize.scale,
        fontWeight: "bold"
    }
});

export default Header;