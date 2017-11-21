import React from 'react';
import {TabNavigator} from 'react-navigation';

import TableContainer from './MainBody/TableContainer';

const ListFile = () => (
    <TableContainer type={"list"}/>
)
const LocalFile = () => (
    <TableContainer type={"local"}/>
)
const RootTabs = TabNavigator({
    ListFile: {
        screen: ListFile,
        navigationOptions: {
            tabBarLabel: '设备文件'
        }
    },
    SelectedFile: {
        screen: LocalFile,
        navigationOptions: {
            tabBarLabel: '已转存文件'
        }
    }
});

export default RootTabs;