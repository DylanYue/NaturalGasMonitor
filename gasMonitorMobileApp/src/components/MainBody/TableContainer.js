import React from 'react';
import {
    Platform,
    StyleSheet,
    Text,
    View,
    ScrollView,
    Dimensions
} from 'react-native';
import moment from 'moment';
import TableRow from './TableRow';
import RNFS from 'react-native-fs';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {fetchFileFromLocal, fetchFileFromServer} from '../../actions/index';
import {removeDuplicate} from '../../utils/index';
import {ANDROID_STORAGE_PATH} from '../../config/config'

let winSize = Dimensions.get('window');

class TableContainer extends React.Component {
    constructor(props) {
        super();
        this.state = {
            fileList: []
        }
    }

    componentDidMount() {
        switch (this.props.type) {
            case "list":
                this.fetchServerFileList();
                break;
            case "local":
                this.fetchLocalFileList();
                break;
        }
    }

    fetchServerFileList() {
        fetch("http://192.168.42.1:3000/getAllFiles")
            .then((response) => response.json())
            .then((responseJSON) => {
                RNFS.readDir(ANDROID_STORAGE_PATH)
                    .then((files) => {
                        let result = removeDuplicate(responseJSON, files);
                        this.props.getServerFiles(result);
                    })
                    .catch((err) => {
                        console.log(err);
                    });
            })
            .catch((error) => {
                console.error(error);
            });
    }

    fetchLocalFileList() {
        RNFS.readDir(ANDROID_STORAGE_PATH)
            .then((files) => {
                var result = files.map(function (val) {
                    return {
                        fileName: val.name,
                        size: (val.size / 1000000).toFixed(2),
                        birthtime: moment(val.mtime).format("YY-MM-DD HH:mm"),
                        duration: "0.0",
                    };
                });
                this.props.getLocalFiles(result)
            })
            .catch((err) => {
                console.log('fetch local file', err.message)
            });
    }

    render() {
        let filesList;
        if (this.props.type === 'list' && this.props.files.serverFiles !== undefined && this.props.files.serverFiles !== null && this.props.files.serverFiles.length !== 0) {
            filesList = (
                <View style={styles.tableContent}>
                    <ScrollView>
                        {this.props.files.serverFiles.map((file, index) => {
                            return <TableRow
                                key={file.fileName}
                                data={{
                                    file,
                                    type: this.props.type
                                }}
                            />
                        })}
                    </ScrollView>
                </View>)
        } else if (this.props.type === 'local' && this.props.files.localFiles !== undefined && this.props.files.localFiles !== null && this.props.files.localFiles.length !== 0) {
            filesList = (
                <View style={styles.tableContent}>
                    <ScrollView>
                        {this.props.files.localFiles.map((file, index) => {
                            return <TableRow
                                key={file.fileName}
                                data={{
                                    file,
                                    type: this.props.type
                                }}
                            />
                        })}
                    </ScrollView>
                </View>)
        }
        return (

            <View style={styles.mainBody}>
                <View style={styles.tableHeader}>
                    <View style={styles.table_fileName}>
                        <Text style={styles.table_headerText}>文件名</Text>
                    </View>
                    <View style={styles.table_size}>
                        <Text style={styles.table_headerText}>MB</Text>
                    </View>
                    <View style={styles.table_createTime}>
                        <Text style={styles.table_headerText}>记录时间</Text>
                    </View>
                    <View style={styles.table_duration}>
                        <Text style={styles.table_headerText}>小时</Text>
                    </View>
                    <View style={styles.table_select}>
                        <Text style={styles.table_headerText}>选择</Text>
                    </View>
                </View>
                {filesList}
            </View>
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
        getLocalFiles: fetchFileFromLocal,
        getServerFiles: fetchFileFromServer
    }, dispatch)
}


const styles = StyleSheet.create({
    mainBody: {
        flex: 1,
    },
    tableHeader: {
        flex: 0.1,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        margin: 10,
        borderWidth: 1,
        borderRadius: 5
    },
    tableContent: {
        flex: 1,
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

export default connect(mapStateToProps, matchDispatchToProps)(TableContainer);