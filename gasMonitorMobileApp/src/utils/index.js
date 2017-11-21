exports.removeDuplicate = function (result, target) {
    let nameSet = target.map((val) => (val.name));
    for (let name of nameSet) {
        result = result.filter(function (val) {
            return val.fileName !== name;
        })
    }
    return result;
}

exports.swapLocalAndServer = function (added, removed, target) {
    let targetObj = {};
    removed = removed.filter((val) => {
        if (val.fileName === target) {
            targetObj = val;
        }
        return val.fileName !== target;
    });
    added.push(targetObj);
    return {added, removed};
}
