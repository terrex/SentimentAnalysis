import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.3
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2

ApplicationWindow {
    id: rootWindow
    objectName: "rootWindow"
    width: 640
    height: 480

    FileDialog {
        id: fileDialogChooseTSV
        objectName: "fileDialogChooseTSV"
        nameFilters: ["Tab-separated files (*.tsv)"]
        onAccepted: {
            console.log("el tipo es:")
            console.log(typeof(fileDialogChooseTSV.fileUrl))
            mainPfcsamrApp.load_tsv(this.fileUrl)
        }
    }

    TextEdit {
        id: txtProgram
        objectName: "txtProgram"
        x: 13
        y: 39
        width: 518
        height: 199
        font.pixelSize: 12
    }

    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem { text: "Open..." }
            MenuItem {
                text: "Open train.tsv..."
                onTriggered: fileDialogChooseTSV.open()
            }
            MenuItem { text: "Close" }
        }

        Menu {
            title: "Edit"
            MenuItem { text: "Cut" }
            MenuItem { text: "Copy" }
            MenuItem { text: "Paste" }
        }
    }

    toolBar: ToolBar {
        RowLayout {
            anchors.fill: parent
            ToolButton {
                id: btnOpenTrain
                objectName: "btnOpenTrain"
                text: qsTr("Open train.tsv")
                onClicked: fileDialogChooseTSV.open()
            }
            ToolButton {
                text: qsTr("Vectorize")
            }
            ToolButton {
                text: qsTr("Remove stopwords")
            }
            ToolButton {
                text: qsTr("Stemmize")
            }
            ToolButton {
                text: qsTr("Lemmatize")
            }
            ToolButton {
                text: qsTr("BOW")
            }
            ToolButton {
                text: qsTr("2-BOW")
            }
        }
    }

}
