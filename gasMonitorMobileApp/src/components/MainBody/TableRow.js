import React from 'react'
import {
    Platform,
    StyleSheet,
    Text,
    View,
    Dimensions,
    Button
} from 'react-native';
import RNFS from 'react-native-fs';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {clickRemove, clickDownLoad} from '../../actions/index'
import {swapLocalAndServer} from '../../utils/index'
import {ANDROID_STORAGE_PATH} from '../../config/config'
import * as Animatable from 'react-native-animatable';

let winSize = Dimensions.get('window');

class TableRow extends React.Component {
    constructor(props) {
        super();
        switch (props.data.type) {
            case "list":
                this.state = {
                    fileName: props.data.file.fileName,
                    size: props.data.file.size,
                    duration: props.data.file.duration,
                    birthtime: props.data.file.birthtime,
                    checked: false,
                    btnTitle: '下载'
                }
                break;
            case "local":
                this.state = {
                    fileName: props.data.file.fileName,
                    size: props.data.file.size,
                    duration: props.data.file.duration,
                    birthtime: props.data.file.birthtime,
                    checked: false,
                    btnTitle: '删除'
                }
                break;
        }
    }

    downloadClick() {
        switch (this.props.data.type) {
            case "list":
                this.fetchAndSaveFile();
                break;
            case "local":
                this.deleteLocalFile();
                break;
        }
    }

    fetchAndSaveFile() {
        fetch("http://192.168.42.1:3000/getFile/" + this.state.fileName)
            .then((response) => response.json())
            .then((responseJSON) => {
                writeToAndroidFolder(responseJSON.file, responseJSON.result);
                let result = swapLocalAndServer(this.props.files.localFiles, this.props.files.serverFiles, responseJSON.file)
                this.props.clickDownLoad(result);
            })
            .catch((error) => {
                console.error(error);
            });
    }

    deleteLocalFile() {
        RNFS.unlink(ANDROID_STORAGE_PATH + this.state.fileName)
            .then(() => {
                let newLocalFiles = this.props.files.localFiles.filter((val) => {
                    return val.fileName != this.state.fileName;
                });
                this.props.clickRemove({serverFiles: this.props.files.serverFiles, localFiles: newLocalFiles});
            })
            .catch((err) => {
                console.log(err);
            });
    }


    render() {
        return (
            <Animatable.View animation="fadeInRight" style={styles.tableRow}>
                <View style={styles.table_fileName}>
                    <Text style={styles.table_headerText}>{this.state.fileName}</Text>
                </View>
                <View style={styles.table_size}>
                    <Text style={styles.table_headerText}>{this.state.size}</Text>
                </View>
                <View style={styles.table_createTime}>
                    <Text style={styles.table_headerText}>{this.state.birthtime}</Text>
                </View>
                <View style={styles.table_duration}>
                    <Text style={styles.table_headerText}>{this.state.duration}</Text>
                </View>
                <View style={styles.table_select}>
                    <Button
                        title={this.state.btnTitle}
                        onPress={this.downloadClick.bind(this)}
                        accessibilityLabel="I dont know"
                    />
                </View>
            </Animatable.View>
        )
    }
}

function mapStateToProps(state) {
    return {
        files: state.files,
    }
}

function matchDispatchToProps(dispatch) {
    return bindActionCreators({
        clickRemove: clickRemove,
        clickDownLoad: clickDownLoad
    }, dispatch)
}


function writeToAndroidFolder(name, content) {
    RNFS.writeFile(ANDROID_STORAGE_PATH + name, content, 'utf8')
        .then(() => {
            console.log('file writen');
        })
        .catch((err) => {
            console.log(err.message)
        });
}

const styles = StyleSheet.create({
    tableRow: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        margin: 10,
        borderWidth: 1,
        borderRadius: 5
    },
    table_fileName: {
        flex: 0.2,
        margin: 2,
    },
    table_size: {
        flex: 0.1,
        margin: 2,
    },
    table_createTime: {
        flex: 0.3,
        margin: 2,
    },
    table_duration: {
        flex: 0.2,
        margin: 2,
    },
    table_select: {
        flex: 0.2,
        margin: 2,
    },
    table_headerText: {
        textAlign: 'center',
        fontSize: 30 / winSize.scale,
    }
});

export default connect(mapStateToProps, matchDispatchToProps)(TableRow);