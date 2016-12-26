var Node = function (num, feature, class_name) { //nodeクラス
    this.num = num;
    this.feature = feature;
    this.class_name = class_name;
}

var Edge = function (now, destination) { //edgeクラス
    this.now = now;
    this.destination = destination;
}

readDotFile = function(arg){
    var node = new Array;
    var edge = new Array;
    var nodeList = new Array;

    var allText = arg.replace(/\r\n|\r/g, "\n"); //改行文字を書き換え
    var lines = allText.split('\n'); //一行ごとに配列に格納

    for (var i = 0; i < lines.length; i++) { //各ノード，エッジをそれぞれnode, edgeに格納
        if (isNaN(lines[i][0])) {
            //各行の先頭が数字ではない場合何もしない
        }
        else{
            if (nodeList.indexOf(lines[i][0]) >= 0) {
                edge.push(lines[i]);
            }
            else {
                node.push(lines[i]);
                nodeList.push(lines[i][0]);
            }
        }
    }

    for (var i = 0; i < node.length; i++) { //node配列にクラスを付与する
        if (node[i].indexOf("<") >= 0) { //node文字列の中に"<"がある場合は途中ノード
            var start = node[i].indexOf("=") + 2;
            var end = node[i].indexOf("ngini") - 1;
            var xlist = (node[i].substring(start, end)).split(" ");
            node[i] = new Node(Number(node[i][0]), xlist[0], false);
    //        //document.write(node[0].feature);
        }
        else { //node文字列の中に"<"がない場合はゴールノード
            var start = node[i].indexOf("nclass");
            var end = node[i].lastIndexOf("]") - 1;
            var className = node[i].substring(start, end).split(" ");
            node[i] = new Node(Number(node[i][0]), false, className[2]);
        }
    }

    for (var i = 0; i < edge.length; i++) {　//edge配列にクラスを付与する
        var l = edge[i].split(" ");
        edge[i] = new Edge(Number(l[0]), Number(l[2]));
    }

    return [node, edge];
}