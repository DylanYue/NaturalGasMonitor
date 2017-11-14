import React, {Component} from 'react';
import {
    Platform,
    StyleSheet,
    Text,
    View
} from 'react-native';
import FileSystem from 'react-native-filesystem';

export default class App extends Component<{}> {
    componentWillMount() {


    }

    getDate() {
        fetch("http://10.145.241.99:3000/getData").then((response) => response.json())
            .then((responseJson) => {
                console.log("get data", responseJson);
            })
            .catch((error) => {
                console.error(error);
            });
    }

    getAndSaveFile() {
        fetch("http://10.145.241.99:3000/getFile").then((response) => {
            console.log("get file", response);
            writeToFile(response._bodyText);
            checkIfFileExists();
            readFile();
            console.log("path is", FileSystem.absolutePath("NaturalGasMonitor/Data.cvs"));
        }).catch((error) => {
            console.error(error);
        });
    }

    render() {
        return (
            <View style={styles.container}>
                <Text style={styles.welcome}>
                    Welcome to React Native!
                </Text>
            </View>
        );
    }
}

async function writeToFile(content) {
    await FileSystem.writeToFile('NaturalGasMonitor/Data.cvs', content);
    console.log('file is written');
}

async function checkIfFileExists() {
    const fileExists = await FileSystem.fileExists('NaturalGasMonitor/Data.cvs');
    const directoryExists = await FileSystem.directoryExists('NaturalGasMonitor');
    console.log(`file exists: ${fileExists}`, __dirname);
    console.log(`directory exists: ${directoryExists}`);
}

async function readFile() {
    const fileContents = await FileSystem.readFile('NaturalGasMonitor/Data.cvs');
    console.log(`read from file: ${fileContents}`);
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F5FCFF',
    },
    welcome: {
        fontSize: 20,
        textAlign: 'center',
        margin: 10,
    },
    instructions: {
        textAlign: 'center',
        color: '#333333',
        marginBottom: 5,
    },
});
