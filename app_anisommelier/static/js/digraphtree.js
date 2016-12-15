var Node = function (num, feature, class_name) { //node�N���X
    this.num = num;
    this.feature = feature;
    this.class_name = class_name;
}

var Edge = function (now, destination) { //edge�N���X
    this.now = now;
    this.destination = destination;
}

readDotFile = function(arg){
    var node = new Array;
    var edge = new Array;
    var nodeList = new Array;

    var allText = arg.replace(/\r\n|\r/g, "\n"); //���s��������������
    var lines = allText.split('\n'); //��s���Ƃɔz��Ɋi�[

    for (var i = 0; i < lines.length; i++) { //�e�m�[�h�C�G�b�W�����ꂼ��node, edge�Ɋi�[
        if (isNaN(lines[i][0])) {
            //�e�s�̐擪�������ł͂Ȃ��ꍇ�������Ȃ�
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

    for (var i = 0; i < node.length; i++) { //node�z��ɃN���X��t�^����
        if (node[i].indexOf("<") >= 0) { //node������̒���"<"������ꍇ�͓r���m�[�h
            var start = node[i].indexOf("=") + 2;
            var end = node[i].indexOf("ngini") - 1;
            var xlist = (node[i].substring(start, end)).split(" ");
            node[i] = new Node(Number(node[i][0]), xlist[0], false);
    //        //document.write(node[0].feature);
        }
        else { //node������̒���"<"���Ȃ��ꍇ�̓S�[���m�[�h
            var start = node[i].indexOf("nclass");
            var end = node[i].lastIndexOf("]") - 1;
            var className = node[i].substring(start, end).split(" ");
            node[i] = new Node(Number(node[i][0]), false, className[2]);
        }
    }

    for (var i = 0; i < edge.length; i++) {�@//edge�z��ɃN���X��t�^����
        var l = edge[i].split(" ");
        edge[i] = new Edge(Number(l[0]), Number(l[2]));
    }

    return [node, edge];
}